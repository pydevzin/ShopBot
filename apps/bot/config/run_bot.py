from apps.bot.config import bot_config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from apps.bot.handlers import setup_handlers



async def main():
    redis = await Redis.from_url(bot_config.REDIS_URL)
    bot  = Bot(token=bot_config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=RedisStorage(redis=redis))

    setup_handlers(dp)

    await dp.start_polling(bot)