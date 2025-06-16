from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from typing import Optional
from ..callback_data import LanguageCallbackData, LanguageEnum, cb_select_language_callback_data, CategoryCallbackData, \
    SubCategoryBackCallbackData
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
            text="⬅️ Orqaga" if user.language == 'uz' else "⬅️ Назад",  # noqa
            callback_data=SubCategoryBackCallbackData(action='back_to_parent', parent_id=back_to_id).pack()
        )

    inline_keyboard.adjust(2)
    return inline_keyboard.as_markup()
