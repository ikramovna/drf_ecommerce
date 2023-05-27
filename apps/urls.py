from django.urls import path

from .views import ProductListCreateAPIView, \
    SearchAPIView, NewCollectionAPIView, BlogListAPIView, AddCardAPIView, UserCardAPIView, DeleteCardAPIView, \
    BlogDetailUpdateAPIView, WishListCreateAPIView, SubscriptionCreateView, ProductPopularListAPIView, \
    ProductDetailRetrieveAPIView, ProductRetrieveUpdateDestroyAPIView, CommentCreateAPIView, CategoryCreateAPIView, \
    NewsListCreateAPIView, WishlistRetrieveDestroyAPIView, SendMailAPIView, SendNewAPIView

urlpatterns = [
    path('news/', NewsListCreateAPIView.as_view(), name='news'),
    path('search/', SearchAPIView.as_view(), name='search'),
    path('product/', ProductListCreateAPIView.as_view(), name='product'),
    path('product_detail/<int:pk>/', ProductDetailRetrieveAPIView.as_view(), name='product_detail'),
    path('popular_product/', ProductPopularListAPIView.as_view(), name='popular_product'),
    path('product-update-delete/<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view(),
         name='products_update_delete'),
    path('comment/', CommentCreateAPIView.as_view(), name='comment'),
    path('category/', CategoryCreateAPIView.as_view(), name='category'),
    path('collection/', NewCollectionAPIView.as_view(), name='collection'),
    path('blog_list/<int:pk>/', BlogListAPIView.as_view(), name='blog'),
    path('blog_detail/', BlogDetailUpdateAPIView.as_view(), name='blog_detail'),
    path('add_card/', AddCardAPIView.as_view(), name='card'),
    path('user_card/', UserCardAPIView.as_view(), name='user_card'),
    path('delete_card/', DeleteCardAPIView.as_view(), name='delete_card'),
    path('wishlist/', WishListCreateAPIView.as_view(), name='wishlist_create'),
    path('wishlist/<int:pk>/', WishlistRetrieveDestroyAPIView.as_view(), name='wishlist_delete'),
    path('send_mail', SendMailAPIView.as_view(), name='send_mail'),
    path('send_new', SendNewAPIView.as_view(), name='send_new'),
    path('subscriptions/', SubscriptionCreateView.as_view(), name='subscription_create'),

]
