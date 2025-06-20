from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework import filters
from apps.adminka.api_endpoints.Categories.serializers import CategorySerializer
from apps.shop.models import Category


class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    filter_backends = [filters.SearchFilter]
    search_fields = ['name_uz', 'name_ru']
