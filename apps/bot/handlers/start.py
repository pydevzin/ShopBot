from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from ..keyboards.inline_button import inline_languages, inline_sub_categories
from ..states import RegistrationStateGroup, CategoryStateGroup
from ...shop.models import User

router = Router()


@router.message(Command('start'))
async def start_command(message: types.Message, state: FSMContext, **data):
    user = data.get('user')
    if user is None:
        await message.answer(
            text=_("Assalomu alaykum, xush kelibsiz"),  # noqa
            reply_markup=types.ReplyKeyboardRemove()
        )
        await state.set_state(RegistrationStateGroup.language)
        return await message.answer(
            text='Tilni tanlang',  # noqa
            reply_markup=inline_languages()
        )

    await  message.answer(
        text=_('kategoriyalardan birini tanlang:'),  # noqa
        reply_markup=await inline_sub_categories(user=user, parent_id=None)  # noqa
    )
    await state.set_state(CategoryStateGroup.main_category)
