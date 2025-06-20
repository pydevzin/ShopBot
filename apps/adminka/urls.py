from django.urls import path
from apps.adminka import api_endpoints

app_name = 'adminka'  # noqa

urlpatterns = [
    path('category/create', api_endpoints.CategoryCreateAPIView.as_view(), name='create-category'),
    path('category/delete/<int:pk>', api_endpoints.CategoryDeleteAPIView.as_view(), name='delete-category'),
    path('category/update/<int:pk>', api_endpoints.CategoryUpdateAPIView.as_view(), name='update-category'),
    path('category/list/', api_endpoints.CategoryListAPIView.as_view(), name='list-category'),
]

urlpatterns += [
    path('product/list', api_endpoints.ProductListView.as_view(), name='product-list'),
    path('product/create', api_endpoints.ProductCreateView.as_view(), name='product-list'),
    path('product/detail/<int:pk>/', api_endpoints.ProductDetailView.as_view(), name='product-detail'),
    path('product/color/create', api_endpoints.ColorVariantCreateView.as_view(), name='product-color-create'),
    path('product/image', api_endpoints.ProductImageCreateView.as_view(), name='product-image'),

]

urlpatterns += [
    path('CartItem/list', api_endpoints.CartItemListView.as_view(), name='cart-list'),
]

urlpatterns += [
    path('users/list', api_endpoints.UserListAPIView.as_view(), name='user-list'),
    path('users/status/<int:pk>/', api_endpoints.UserStatusUpdateAPIView.as_view(), name='user-status-update'),
    path('users/inactive', api_endpoints.InactiveUserListAPIView.as_view(), name='inactive-users'),
    path('users/active', api_endpoints.ActiveUserListAPIView.as_view(), name='active-users'),
]
