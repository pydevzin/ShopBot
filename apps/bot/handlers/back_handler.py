from aiogram import Router, types
from aiogram.utils.i18n import gettext as _

from ..callback_data import SubCategoryBackCallbackData, MainMenuBackCallbackData, CartItemBackCallbackData
from ..keyboards.inline_button import inline_sub_categories

router = Router()


# ichki kategoriyadan bitta ortga qaytish
@router.callback_query(SubCategoryBackCallbackData.filter())
async def back_to_parent_callback(callback: types.CallbackQuery, callback_data: SubCategoryBackCallbackData, **data):
    user = data.get('user')
    parent_id = callback_data.parent_id

    try:
        await callback.message.delete()
    except Exception as e:
        pass

    await callback.message.answer(
        text=_("Kategoriyalardan birini tanlang:"),  # noqa
        reply_markup=await inline_sub_categories(user=user, parent_id=parent_id)
    )


# to'g'ridan to'g'ri asosiy menuga qaytish
@router.callback_query(MainMenuBackCallbackData.filter())
async def back_main_menu_callback(callback: types.CallbackQuery, callback_data: MainMenuBackCallbackData, **data):
    user = data.get('user')
    await callback.message.edit_text(
        text=_('Kategoriyalardan birini tanlang:'),  # noqa
        reply_markup=await inline_sub_categories(user=user, parent_id=None)
    )

# cart item (savatcha) ichida asosiy menuga qaytish
@router.callback_query(CartItemBackCallbackData.filter())
async def cart_item_back_main_menu(callback: types.CallbackQuery, callback_data: CartItemBackCallbackData, **data):
    user = data.get('user')
    await callback.message.answer(
        text=_('Kategoriyalardan birini tanlang:'),  # noqa
        reply_markup=await inline_sub_categories(user=user, parent_id=None)
    )
