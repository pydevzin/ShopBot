from django.contrib import admin
from .models import User, Category, Product, ProductImage, ColorVariant


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['password', 'language', 'phone_number']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    pass
