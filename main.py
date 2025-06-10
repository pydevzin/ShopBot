import asyncio
import logging
from loguru import logger
from apps.bot.config.run_bot import main as run_bot


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    event_loop = asyncio.get_event_loop()

    try:
        event_loop.create_task(run_bot())
        event_loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Bot Stopped")
        event_loop.stop()
    finally:
        event_loop.close()
    # try:
    #     asyncio.run(run_bot())
    # except KeyboardInterrupt:
    #     logger.info("Bot Stopped")