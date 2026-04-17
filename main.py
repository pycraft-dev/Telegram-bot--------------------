"""Точка входа: запуск Telegram-бота (polling)."""

import asyncio
import logging

from aiogram import Bot, Dispatcher

from src.config import load_config
from src.handlers.main import build_root_router
from src.logging_setup import setup_logging


async def main() -> None:
    """Запускает бота в режиме polling."""

    setup_logging()

    config = load_config()
    bot = Bot(token=config.bot_token)

    dp = Dispatcher()
    dp.include_router(build_root_router())

    logging.getLogger(__name__).info("Bot started (polling)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

