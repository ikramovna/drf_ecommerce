from django.db.models import Model, TextField, CharField, IntegerField, ForeignKey, ImageField, CASCADE, TextChoices, \
    DateTimeField, EmailField

from django.utils.translation import gettext_lazy as _
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Product(Model):
    title = CharField(max_length=255)
    price = IntegerField()
    description = TextField(blank=True, null=True)
    discount = IntegerField(blank=True, null=True)

    class Availability(TextChoices):
        IN_STOCK = 'in stock', 'In stock'
        OUT_OF_STOCK = 'out of stock', 'Out of stock'

    availability = CharField(max_length=15, choices=Availability.choices)
    quantity = IntegerField()
    category = ForeignKey('apps.Category', on_delete=CASCADE)
    created_at = DateTimeField(auto_now_add=True)
    views = IntegerField(default=0)
    option = ForeignKey('apps.Option', CASCADE, null=True)

    def __str__(self):
        return self.title


class ProductImage(Model):
    product = ForeignKey('apps.Product', CASCADE)
    image = ImageField(upload_to='products/images/')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')


class Comment(Model):
    author = ForeignKey('auth.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)
    job = CharField(max_length=255)
    text = TextField()
    image = ImageField(upload_to='comment/images/')


class Category(MPTTModel, Model):
    name = CharField(max_length=255)
    parent = TreeForeignKey('self', CASCADE, 'children', null=True, blank=True)

    def __str__(self):
        return self.name


class New(Model):
    title = CharField(max_length=255)
    description = TextField()
    comment = ForeignKey('apps.Comment', on_delete=CASCADE)
    image = ImageField(upload_to='news/')
    created_at = DateTimeField(auto_now_add=True)
    user = ForeignKey('auth.User', default='auth.User', on_delete=CASCADE)


class Card(Model):
    product = ForeignKey('apps.Product', CASCADE)
    quantity = IntegerField(default=1)
    user = ForeignKey('auth.User', CASCADE)
    date = DateTimeField(auto_now_add=True)


class Wishlist(Model):
    product = ForeignKey('apps.Product', CASCADE)
    user = ForeignKey('auth.User', CASCADE)
    created_at = DateTimeField(auto_now=True)


class Subscribe(Model):
    email = EmailField()
    subscribe_at = DateTimeField(auto_now_add=True)


class Option(Model):
    brand = CharField(max_length=50),
    season = CharField(max_length=50),
    color = CharField(max_length=50),
    fit = CharField(max_length=50),
    size = CharField(5)
