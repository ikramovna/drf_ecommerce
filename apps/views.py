from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, CreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Product, Comment, Category, New, Card, Wishlist, Subscribe
from apps.serializers import ProductModelSerializer, CommentModelSerializer, CategoryModelSerializer, \
    NewModelSerializer, NewCollectionSerializer, BlogListSerializer, SearchSerializer, CardSerializer, \
    CardDetailSerializer, WishListSerializer, SendEmailSerializer, SubscriptionSerializer, SendNewSerializer
from apps.tasks import send_email_customer


# ProductDetail
class ProductDetailRetrieveAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer


# Create
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_fields = ('category', 'price', 'option__color')

    # filterset_class = ProductFilter


# Update and Delete
class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()[:9]
    serializer_class = ProductModelSerializer


# Comment
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer


# Subscription
class SubscriptionCreateView(CreateAPIView):
    queryset = Subscribe.objects.all()
    serializer_class = SubscriptionSerializer


# Category
class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer


# Last news
class NewsListCreateAPIView(ListCreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewModelSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)


# Blog List
class BlogListAPIView(ListAPIView):
    queryset = New.objects.all()
    serializer_class = BlogListSerializer


# Blog Detail
class BlogDetailUpdateAPIView(UpdateAPIView):
    queryset = New.objects.all()
    serializer_class = ProductModelSerializer


# WishList create

class WishListCreateAPIView(CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListSerializer


# WishList Delete
class WishlistRetrieveDestroyAPIView(RetrieveDestroyAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishListSerializer


# Search
class SearchAPIView(APIView):

    @swagger_auto_schema(query_serializer=SearchSerializer)
    def get(self, request):
        q = request.GET.get('title', None)
        print(q)
        posts = Product.objects.filter(title__iexact=q)
        serializer = ProductModelSerializer(posts, many=True)
        return Response(serializer.data)


# Popular product
class ProductPopularListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer

    def get_queryset(self):
        query = super().get_queryset().order_by('-views')
        return query


# New Collection
class NewCollectionAPIView(APIView):
    def get(self, request):
        expiry_date = timezone.now() - timedelta(days=5)
        products = Product.objects.filter(Q(created_at__gte=expiry_date) & Q(created_at__lte=timezone.now()))
        serializer = NewCollectionSerializer(products, many=True)

        return Response(serializer.data, status=200)


# Shopping Card
class AddCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.data._mutable = True
        request.data['user'] = request.user.id
        serializer = CardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=201)


class UserCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_product = Card.objects.filter(user=request.user)
        serializer = CardDetailSerializer(user_product, many=True)
        summ = 0
        for element in serializer.data:
            summ += element['product']['price'] * element['quantity']
        data = {
            'data': serializer.data,
            'summ': summ
        }
        return Response(data)


class DeleteCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            Card.objects.get(Q(pk=pk), Q(user=request.user)).delete()
        except Card.DoesNotExist:
            return Response({'message': 'This product does not exist'})
        return Response(status=204)


# Celery SendMail

class SendMailAPIView(APIView):
    def post(self, request):
        try:
            serializer = SendEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            message = serializer.validated_data.get('message')
            name = serializer.validated_data.get('name')
            phone = serializer.validated_data.get('phone')

            send_email_customer.delay(email, message, name, phone)
        except Exception as e:
            return Response({'success': False, 'message': str(e)})

        return Response({'success': True, 'message': 'Email sent!'})


# Send news to user_email
class SendNewAPIView(APIView):
    def post(self, request):
        try:
            serializer = SendNewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            pk = serializer.validated_data.get('pk')

            send_email_customer.delay(pk)
        except Exception as e:
            return Response({'success': False, 'message': str(e)})

        return Response({'success': True, 'message': 'Email sent!'})
