from enum import Enum
from sys import prefix
from typing import Optional
from aiogram.filters.callback_data import CallbackData


class LanguageEnum(str, Enum):
    UZ = 'uz'
    RU = 'ru'


class LanguageCallbackData(CallbackData, prefix='language_prefix'):
    language: LanguageEnum


def cb_select_language_callback_data(lang):
    return LanguageCallbackData(language=lang.value).pack()


class CategoryCallbackData(CallbackData, prefix='category_prefix'):
    category_id: int


class SubCategoryBackCallbackData(CallbackData, prefix='sub_category_back_prefix'):
    action: str
    parent_id: Optional[int]


class MainMenuBackCallbackData(CallbackData, prefix='back_main_menu_prefix'):
    action: str


class ProductCallbackData(CallbackData, prefix='product_prefix'):
    product_id: int



class ProductImageCallbackData(CallbackData, prefix='product_image'):
    product_id: int
    image_index: int


class AddToCartCallbackData(CallbackData, prefix="add_cart"):
    product_id : int
    color_variant_id: int




class CartImageCallbackData(CallbackData, prefix="cart_prefix"):
    index: int


class RemoveCartItemCallbackData(CallbackData, prefix='remove_cart_prefix'):
    current_item_id : int



class CartItemBackCallbackData(CallbackData, prefix='cart_item_back_prefix'):
    action: str

#
#
#
# class OrderCallbackData(CallbackData, prefix="order_prefix"):
#     product_id: int
#
#
# class ColorVariantCallbackData(CallbackData, prefix="color"):
#     product_id: int
#     color_variant_id: int
#
#
#
#
# class CartCallbackData(CallbackData, prefix="cart"):
#     # action: str  # "view", "remove", "increase", "decrease"
#     product_id: int = 0
#
#
# class QuantityCallbackData(CallbackData, prefix="quantity"):
#     color_variant_id: int
#     quantity: int
