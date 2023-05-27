from django.contrib import admin

from .models import Category, Product, New, ProductImage
from .tasks import send_email_customer, send_email_customer1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')


admin.site.register(Category, CategoryAdmin)


class NewAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        send_email_customer1.apply_async(args=[self, request, obj, form])


admin.site.register(New, NewAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'product']


admin.site.register(ProductImage, ProductImageAdmin)
