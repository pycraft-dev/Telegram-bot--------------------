"""Хендлеры команды /start."""

import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.keyboards import main_menu_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Отправляет приветствие и главное меню."""

    user_id = message.from_user.id if message.from_user else None
    logger.info("Received /start from user_id=%s", user_id)

    await message.answer(
        "Привет!\n\nЧтобы получить гайд, нужно подписаться на канал.",
        reply_markup=main_menu_keyboard(),
    )

