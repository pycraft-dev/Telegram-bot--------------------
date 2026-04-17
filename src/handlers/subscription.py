"""Хендлеры проверки подписки и выдачи гайда."""

import logging

from aiogram import Bot, F, Router
from aiogram.types import FSInputFile, Message

from src.config import load_config
from src.keyboards import channel_link_keyboard, main_menu_keyboard
from src.utils.checks import is_subscribed

router = Router()
logger = logging.getLogger(__name__)


async def _send_guide(message: Message, bot: Bot) -> None:
    """Отправляет PDF-гайд пользователю (если файл доступен)."""

    config = load_config()
    guide_path = config.guide_path

    if not guide_path.exists() or not guide_path.is_file():
        logger.error("Guide file not found: %s", guide_path)
        await message.answer(
            "Гайд пока недоступен. Пожалуйста, попробуйте позже.",
            reply_markup=main_menu_keyboard(),
        )
        return

    document = FSInputFile(path=guide_path)
    await message.answer_document(
        document=document,
        caption="Ваш гайд (PDF).",
        reply_markup=main_menu_keyboard(),
    )
    logger.info("Guide sent to user_id=%s", message.from_user.id if message.from_user else None)


@router.message(F.text == "Подписаться")
async def on_subscribe_button(message: Message, bot: Bot) -> None:
    """Обрабатывает нажатие кнопки «Подписаться»."""

    config = load_config()
    user_id = message.from_user.id if message.from_user else None
    logger.info("Subscribe button pressed by user_id=%s", user_id)

    await message.answer(
        "Перейдите в канал и подпишитесь, затем нажмите «Проверить подписку».",
        reply_markup=channel_link_keyboard(channel_link=config.channel_link),
    )


@router.message(F.text == "Проверить подписку")
async def on_recheck_button(message: Message, bot: Bot) -> None:
    """Повторно проверяет подписку и выдаёт гайд при успехе."""

    config = load_config()
    user_id = message.from_user.id if message.from_user else None
    logger.info("Recheck button pressed by user_id=%s", user_id)

    if user_id is None:
        await message.answer("Не удалось определить пользователя. Попробуйте ещё раз.")
        return

    subscribed = await is_subscribed(bot=bot, channel_id=config.channel_id, user_id=user_id)
    if subscribed:
        await _send_guide(message=message, bot=bot)
        return

    await message.answer(
        "Пока не вижу подписку.\n\nПерейдите в канал, подпишитесь и попробуйте снова.",
        reply_markup=channel_link_keyboard(channel_link=config.channel_link),
    )

