from aiogram import Router, types, F
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from aiogram.utils.i18n import gettext as _

from apps.shop.models import User
from ..callback_data import LanguageCallbackData
from ..keyboards.inline_button import inline_sub_categories
from ..keyboards.reply_button import reply_phone_number
from ..states import RegistrationStateGroup, CategoryStateGroup

router = Router()


@router.callback_query(LanguageCallbackData.filter())
async def start_register(callback_query: types.CallbackQuery,
                         state: FSMContext,
                         callback_data: LanguageCallbackData,
                         ):
    await state.update_data({'language': callback_data.language})

    # await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.answer(_('Ismingizni kiriting:'),  # noqa
                                        reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegistrationStateGroup.fullname)


@router.message(F.text, RegistrationStateGroup.fullname)
async def fullname_register(message: types.Message, state: FSMContext):
    await state.update_data({'fullname': message.text})
    await message.answer(_('Telefon raqamingizni yuboring:'),  # noqa
                         reply_markup=reply_phone_number())
    await state.set_state(RegistrationStateGroup.phone)


@router.message(or_f(F.text, F.contact), RegistrationStateGroup.phone)
async def receive_phone(message: types.Message, state: FSMContext):
    phone_number = None
    if message.text:
        if not message.text.startswith('+998') or len(message.text) != 13:
            return message.answer(_("To`g`ri formatda raqam jo`nating yoki buttondan foydalaning"))  # noqa
        phone_number = message.text

    elif message.contact:
        phone_number = message.contact.phone_number

    if phone_number:
        await state.update_data({"phone_number": phone_number})
        user_data = await state.get_data()

        await User.objects.bot_create_user(phone_number=user_data['phone_number'],
                                           fullname=user_data['fullname'],
                                           language=user_data['language'],
                                           telegram_id=message.from_user.id
                                           )
        await message.answer("✅", reply_markup=types.ReplyKeyboardRemove())
        user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)

        await message.answer(
            text=_('kategoriyalardan birini tanlang:'),  # noqa
            reply_markup=await inline_sub_categories(user=user, parent_id=None)
        )

        await state.set_state(CategoryStateGroup.main_category)
        await state.clear()
