from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .models import User, Category, Product, ProductImage, ColorVariant, CartItem


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['password', 'language', 'phone_number']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name_uz']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ColorVariantInline(admin.TabularInline):
    model = ColorVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(ColorVariant)
class ColorVariantAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['product', 'price', 'show_image']

    # @admin.display(description="ko'rinish")  # noqa
    # def str_display(self, obj):
    #     return str(obj)

    @admin.display(description="image")
    def show_image(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;" />',
                               first_image.image.url)
        return "Rasm yo‘q"


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user','product','color_variant' ]
    readonly_fields = ['user', 'product','color_variant']

    @admin.display(description='image')
    def show_image(self, obj):
        ...
