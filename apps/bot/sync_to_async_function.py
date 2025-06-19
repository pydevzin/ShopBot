from asgiref.sync import sync_to_async
from apps.shop.models import Product, Category, User, CartItem


@sync_to_async
def get_has_category_children(category_id: int) -> bool:
    return Category.objects.filter(parent_id=category_id).exists()


@sync_to_async
def get_product_with_colors(product_id: int):
    try:
        return Product.objects.only("name_uz", "name_ru").prefetch_related("colors__images").get(id=product_id)
    except Product.DoesNotExist:  # noqa
        return None


@sync_to_async
def get_user_obj(user_id: int):
    return User.objects.filter(telegram_id=user_id).first()


@sync_to_async
def get_existing_item(user_obj, color_variant):
    return CartItem.objects.filter(user=user_obj, color_variant=color_variant).exists()


@sync_to_async
def get_cart_items(user_obj):
    return list(
        CartItem.objects
        .select_related("product", "color_variant")
        .prefetch_related("color_variant__images")
        .filter(user=user_obj)
    )



@sync_to_async
def get_cart_items_simple(user_obj):
    return list(
        CartItem.objects
        .select_related("product", "color_variant")
        .filter(user=user_obj)
    )

#
# from django.utils.translation import activate, gettext
#
# def get_translated_text(text: str, language: str = 'uz'):
#     activate(language)
#     return gettext(text)