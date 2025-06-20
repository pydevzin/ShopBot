from rest_framework import serializers

from apps.shop.models import Product, ColorVariant, ProductImage,CartItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name_uz', 'name_ru', ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ColorVariantSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = ColorVariant
        fields = ['id', 'color_name', 'price', 'images']

class ProductColorVariantSerializer(serializers.ModelSerializer):
    colors = ColorVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name_uz', 'name_ru', 'categories', 'colors']

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name_uz', 'name_ru', 'categories']

class ColorVariantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVariant
        fields = ['product', 'color_name', 'price']

class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['color_variant', 'image']
