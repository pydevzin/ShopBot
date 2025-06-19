from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async

from ..callback_data import LanguageEnum, cb_select_language_callback_data, CategoryCallbackData, \
    SubCategoryBackCallbackData, MainMenuBackCallbackData, ProductCallbackData, ProductImageCallbackData, \
    AddToCartCallbackData, CartImageCallbackData, RemoveCartItemCallbackData, CartItemBackCallbackData
from ...shop.models import Category, User


def inline_languages():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text='🇺🇿uz', callback_data=cb_select_language_callback_data(lang=LanguageEnum.UZ))
    inline_keyboard.button(text='🇷🇺ru', callback_data=cb_select_language_callback_data(lang=LanguageEnum.RU))

    return inline_keyboard.as_markup()


@sync_to_async
def inline_sub_categories(user: Optional[User], parent_id=None):
    inline_keyboard = InlineKeyboardBuilder()

    if parent_id is None:
        categories = Category.objects.filter(parent_id=None)
    else:
        categories = Category.objects.filter(parent_id=parent_id)

    user_language = user.language if user else 'uz'

    for category in categories:
        has_children = category.children.exists()
        category_text = category.get_name(user_language)
        if has_children:
            category_text += " 📁"

        inline_keyboard.button(
            text=category_text,
            callback_data=CategoryCallbackData(category_id=category.id).pack()
        )

    if parent_id is not None:
        parent_category = Category.objects.filter(id=parent_id).first()
        back_to_id = parent_category.parent_id if parent_category else None

        inline_keyboard.button(
            text="⬅️ Orqaga" if (user and user.language == 'uz') else "⬅️ Назад",  # noqa
            callback_data=SubCategoryBackCallbackData(action='back_to_parent', parent_id=back_to_id).pack()
        )
        inline_keyboard.button(
            text="Asosiy menu 🏠" if (user and user.language == 'uz') else "Главное меню 🏠",  # noqa
            callback_data=MainMenuBackCallbackData(action="back_main_menu").pack()
        )

    inline_keyboard.button(
        text="️🛒 Savatcham" if (user and user.language == 'uz') else "🛒 Корзина",  # noqa
        callback_data="view_cart"
    )

    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()


@sync_to_async
def inline_products_by_category(user: Optional[User], category_id: int):
    inline_keyboard = InlineKeyboardBuilder()

    user_language = user.language if user else 'uz'
    category = Category.objects.filter(id=category_id).first()
    if not category:
        return inline_keyboard.as_markup()

    products = category.products.only('id', 'name_uz', 'name_ru').all()

    for product in products:
        product_text = product.name_ru if user_language == 'ru' else product.name_uz
        product_text += " 📦"
        inline_keyboard.button(
            text=product_text,
            callback_data=ProductCallbackData(product_id=product.id).pack()
        )

    inline_keyboard.button(
        text="⬅️ Orqaga" if (user and user.language == 'uz') else "⬅️ Назад",  # noqa
        callback_data=SubCategoryBackCallbackData(action='back_to_parent', parent_id=category.parent_id).pack()
    )
    inline_keyboard.button(
        text="Asosiy menu 🏠" if (user and user.language == 'uz') else "Главное меню 🏠",  # noqa
        callback_data=MainMenuBackCallbackData(action="back_main_menu").pack()
    )

    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()


@sync_to_async
def product_images_keyboard(product, current_index, language='uz'):
    keyboard = InlineKeyboardBuilder()

    all_images = [
        (img, color.id) for color in product.colors.all()
        for img in color.images.all()
    ]
    total_images = len(all_images)

    if current_index > 0:
        keyboard.button(
            text="◀️" if language == "uz" else "◀️",  # noqa
            callback_data=ProductImageCallbackData(product_id=product.id, image_index=current_index - 1).pack()
        )

    if current_index < total_images - 1:
        keyboard.button(
            text="▶️" if language == "uz" else "▶️",  # noqa
            callback_data=ProductImageCallbackData(product_id=product.id, image_index=current_index + 1).pack()
        )

    _, color_variant_id = all_images[current_index]

    keyboard.button(
        text="🛍️ buyurtma berish" if language == "uz" else "🛍️ размещение заказа",  # noqa
        callback_data="buyurtma_berish"  # noqa
    )

    keyboard.button(
        text="🛒 savatga qo'shish" if language == "uz" else "🛒 добавить в корзину",  # noqa
        callback_data=AddToCartCallbackData(product_id=product.id, color_variant_id=color_variant_id).pack()
    )

    keyboard.button(
        text="⬅️ Ortga" if language == 'uz' else "⬅️ Назад",  # noqa
        callback_data=CategoryCallbackData(category_id=product.categories_id).pack()
    )

    keyboard.adjust(2)
    return keyboard.as_markup()








@sync_to_async
def cart_images_keyboard(cart_items, current_index, language='uz'):
    keyboard = InlineKeyboardBuilder()

    if current_index > 0:
        keyboard.button(
            text="◀️",
            callback_data=CartImageCallbackData(index=current_index - 1).pack()
        )

    if current_index < len(cart_items) - 1:
        keyboard.button(
            text="▶️",
            callback_data=CartImageCallbackData(index=current_index + 1).pack()
        )

    current_item = cart_items[current_index]

    keyboard.button(
        text="🛍️ Buyurtma berish" if language == 'uz' else "🛍️ Разместить заказ", # noqa
        callback_data="buyurtma_berish" # noqa
    )

    keyboard.button(
        text="➖ O'chirish" if language == 'uz' else "➖ Удалить", # noqa
        callback_data=RemoveCartItemCallbackData(current_item_id=current_item.id),
    )

    keyboard.button(
        text="Asosiy menu 🏠" if language == 'uz' else "Главное меню",  # noqa
        callback_data=CartItemBackCallbackData(action="back_main_menu").pack()
    )

    keyboard.adjust(2)
    return keyboard.as_markup()



@sync_to_async
def cart_empty_keyboard(user):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(
        text="🏠 Asosiy menu" if user.language == 'uz' else "🏠 Главное меню",    # noqa
        callback_data=CartItemBackCallbackData(action="back_main_menu").pack()
    )
    return keyboard.as_markup()


