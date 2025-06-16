from apps.bot.config import bot_config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiogram.utils.i18n import I18n, FSMI18nMiddleware

from aiogram.utils.i18n import I18n, I18nMiddleware
from aiogram.enums.parse_mode import ParseMode

from apps.bot.handlers import setup_handlers
from apps.bot.middlewares.check_registration import UserMiddleware
from apps.bot.middlewares.language import CustomFSMII18nMiddleware

user_middleware = UserMiddleware()

async def main():
    redis = await Redis.from_url(bot_config.REDIS_URL)
    bot = Bot(token=bot_config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=RedisStorage(redis=redis))

    i18n = I18n(path="locales", default_locale="uz", domain="messages")
    dp.update.middleware(CustomFSMII18nMiddleware(i18n))
    dp.message.middleware(user_middleware)
    setup_handlers(dp)

    await dp.start_polling(bot)
