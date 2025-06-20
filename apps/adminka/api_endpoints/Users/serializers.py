from rest_framework import serializers

from apps.shop.models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'fullname', 'phone_number', 'telegram_id', 'language', 'is_active']

class UserStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']