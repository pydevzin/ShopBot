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
