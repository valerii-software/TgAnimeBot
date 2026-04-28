import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest

from core.config import settings
from core.db.database import SessionLocal, init_models
from core.handlers import basic, core
from core.message_texts import start_bot_message, stop_bot_message
from core.middlewares.db_middleware import DbSessionMiddleware
from core.utils.commands import set_commands


async def on_startup(bot: Bot):
    await set_commands(bot=bot)
    try:
        await bot.send_message(chat_id=settings.admin_id, text=start_bot_message)
    except TelegramBadRequest:
        logging.warning("Could not notify admin on startup (chat not found). Send /start to the bot first.")


async def on_shutdown(bot: Bot):
    try:
        await bot.send_message(chat_id=settings.admin_id, text=stop_bot_message)
    except TelegramBadRequest:
        logging.warning("Could not notify admin on shutdown (chat not found).")


async def main():
    log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler("logs/anime_logs", mode="a")
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)

    await init_models()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.update.middleware(DbSessionMiddleware(session_pool=SessionLocal))

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_router(basic.router)
    dp.include_router(core.router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
