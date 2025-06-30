from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import I18n
from redis.asyncio.client import Redis

from apps.bot.config import bot_config
from apps.bot.handlers import setup_handlers
from apps.bot.middlewares.check_registration import UserMiddleware
from apps.bot.middlewares.language import CustomFSMII18nMiddleware

user_middleware = UserMiddleware()
bot = None
dp = None


async def init_aiogram():
    global bot, dp
    if bot is not None and dp is not None:
        return bot, dp
    redis = await Redis.from_url(bot_config.REDIS_URL)
    storage = RedisStorage(redis=redis)
    bot = Bot(token=bot_config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)
    i18n = I18n(path="locales", default_locale="uz", domain="messages")
    dp.update.middleware(CustomFSMII18nMiddleware(i18n))
    dp.message.middleware(user_middleware)
    dp.callback_query.middleware(user_middleware)
    setup_handlers(dp)
    await bot.set_webhook(bot_config.WEBHOOK_URL)
    print(f"Webhook set to: {bot_config.WEBHOOK_URL}")
    return bot, dp


async def get_bot_and_dp():
    global bot, dp
    if bot is None or dp is None:
        await init_aiogram()
    return bot, dp


""" polling uchun : """  # noqa
# async def main():
#     redis = await Redis.from_url(bot_config.REDIS_URL)
#     bot = Bot(token=bot_config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#     dp = Dispatcher(storage=RedisStorage(redis=redis))
#
#     i18n = I18n(path="locales", default_locale="uz", domain="messages")
#     dp.update.middleware(CustomFSMII18nMiddleware(i18n))
#     dp.message.middleware(user_middleware)
#     dp.callback_query.middleware(user_middleware)
#     setup_handlers(dp)
#
#     await dp.start_polling(bot)
