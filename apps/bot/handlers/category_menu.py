from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import I18n
i18n = I18n(path='locales', default_locale='uz', domain='messages')



from ..callback_data import CategoryCallbackData
from ..keyboards.inline_button import inline_sub_categories, inline_products_by_category
from ..states import CategoryStateGroup
from ..sync_to_async_function import get_has_category_children

router = Router()


@router.callback_query(CategoryCallbackData.filter())
async def category_callback_handler(callback: types.CallbackQuery, callback_data: CategoryCallbackData,
                                    state: FSMContext, **data):
    user = data.get('user')
    category_id = callback_data.category_id

    has_children = await get_has_category_children(category_id)

    try:
        await callback.message.delete()
    except Exception:
        pass

    if has_children:
        await callback.message.answer(
            text=_("Ichki kategoriyalardan birini tanlang:"),  # noqa
            reply_markup=await inline_sub_categories(user=user, parent_id=category_id)
        )
        await state.set_state(CategoryStateGroup.sub_category)
    else:
        await callback.message.answer(
            text=_("Mahsulotlardan birini tanlang:"),  # noqa
            reply_markup=await inline_products_by_category(user=user, category_id=category_id)
        )
        await state.set_state(CategoryStateGroup.product_list)
