from typing import Callable, Awaitable, Dict, Any, Union
from aiogram import types, BaseMiddleware, Bot
from asgiref.sync import sync_to_async

from apps.bot.keyboards.inline_button import inline_languages
from apps.bot.states import RegistrationStateGroup
from apps.shop.models import User


class UserMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable,
                       event: Union[types.Message, types.CallbackQuery, types.InlineQuery],
                       data: Dict[str, Any]
                       ) -> Any:

        bot: Bot = data['bot']
        state = data['state']
        current_state = await state.get_state()

        user = None
        if hasattr(event, 'from_user') and event.from_user:
            telegram_id = event.from_user.id
            user = await sync_to_async(User.objects.filter(telegram_id=telegram_id).first)()

        data['user'] = user

        if current_state in [
            RegistrationStateGroup.language,
            RegistrationStateGroup.fullname,
            RegistrationStateGroup.phone
        ]:
            return await handler(event, data)

        if user is None:
            chat_id = event.from_user.id

            await event.answer("Iltimos, avval ro'yxatdan o'ting")  # noqa

            await bot.send_message(
                chat_id=chat_id,
                text="Iltimos, avval ro'yxatdan o'ting.",  # noqa
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.set_state(RegistrationStateGroup.language)
            await bot.send_message(
                chat_id=chat_id,
                text="Tilni tanlang:",  # noqa
                reply_markup=inline_languages()
            )

            return

        return await handler(event, data)
