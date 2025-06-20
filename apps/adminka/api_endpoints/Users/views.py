from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from apps.shop.models import User
from .serializers import UserListSerializer, UserStatusUpdateSerializer


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]


class UserStatusUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserStatusUpdateSerializer
    permission_classes = [IsAdminUser]


class ActiveUserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(is_active=True)


class InactiveUserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(is_active=False)