from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from apps.adminka.api_endpoints.Cart.serializers import CartItemSerializer
from apps.shop.models import CartItem


class CartItemListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

