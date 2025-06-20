from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

from apps.shop.models import Product, ColorVariant, ProductImage
from .serializers import (
    ProductSerializer, ProductCreateUpdateSerializer,
    ColorVariantCreateSerializer,
    ProductImageCreateSerializer
)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAdminUser]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [IsAdminUser]


class ColorVariantCreateView(generics.CreateAPIView):
    queryset = ColorVariant.objects.all()
    serializer_class = ColorVariantCreateSerializer
    permission_classes = [IsAdminUser]


class ProductImageCreateView(generics.CreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageCreateSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
