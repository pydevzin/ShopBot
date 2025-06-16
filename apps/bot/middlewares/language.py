from typing import Dict, Any

from aiogram.utils.i18n.middleware import FSMI18nMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext


class CustomFSMII18nMiddleware(FSMI18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        state: FSMContext = data.get("state")
        if state:
            user_data = await state.get_data()
            return user_data.get("language", self.i18n.default_locale)
        return self.i18n.default_locale
