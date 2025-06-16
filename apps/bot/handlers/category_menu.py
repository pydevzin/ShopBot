from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _, I18n

from aiogram.utils.i18n.middleware import I18nMiddleware
from aiogram.filters import or_f
from ..callback_data import LanguageCallbackData, CategoryCallbackData, SubCategoryBackCallbackData
from ..keyboards.inline_button import inline_sub_categories
from ..states import RegistrationStateGroup, CategoryStateGroup
from apps.shop.models import User
from ..keyboards.reply_button import reply_phone_number

router = Router()


@router.callback_query(CategoryCallbackData.filter())
async def category_callback_handler(callback: types.CallbackQuery, callback_data: CategoryCallbackData,
                                    state: FSMContext, **data):

    # user = data.get('user')
    user = await User.objects.aget(telegram_id=callback.from_user.id)
    print(f"category handler user >>>> {user}")
    category_id = callback_data.category_id
    await callback.message.edit_text(
        text=_("Ichki kategoriyalardan birini tanlang:"),  # noqa
        reply_markup=await inline_sub_categories(user=user, parent_id=category_id)
    )
    await state.set_state(CategoryStateGroup.sub_category)


@router.callback_query(SubCategoryBackCallbackData.filter())
async def back_to_parent_callback(callback: types.CallbackQuery, callback_data: SubCategoryBackCallbackData, **data):
    user = await User.objects.aget(telegram_id=callback.from_user.id)
    parent_id = callback_data.parent_id
    await callback.message.edit_text(
        text=_("Kategoriyalardan birini tanlang:"),  # noqa
        reply_markup=await inline_sub_categories(user=user, parent_id=parent_id)
    )
