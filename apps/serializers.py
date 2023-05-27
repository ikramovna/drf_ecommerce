from rest_framework.fields import EmailField, CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer

from .models import ProductImage, Product, Comment, Category, New, Card, Wishlist, Subscribe


class ProductImageModelSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductModelSerializer(ModelSerializer):
    images = ProductImageModelSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NewModelSerializer(ModelSerializer):
    class Meta:
        model = New
        exclude = ()


class NewCollectionSerializer(ModelSerializer):
    class Meta:
        model = Product
        exclude = ()


class BlogDetailSerializer(ModelSerializer):
    class Meta:
        model = New
        fields = '__all__'


class BlogListSerializer(ModelSerializer):
    class Meta:
        model = New
        fields = ('title', 'description')


class WishListSerializer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'


class SearchSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('title',)


class ProductSerializerForCard(ModelSerializer):
    class Meta:
        model = Product
        fields = ('title', 'price', 'category')


class CardSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = ('product', 'quantity', 'user', 'date')


class CardDetailSerializer(ModelSerializer):
    product = ProductSerializerForCard()

    class Meta:
        model = Card
        fields = ('product', 'quantity')


class SendNewSerializer(Serializer):
    pk = IntegerField()


class SendEmailSerializer(Serializer):
    message = CharField(max_length=500)
    name = CharField(max_length=100)
    phone = CharField(max_length=55)
    email = EmailField()
