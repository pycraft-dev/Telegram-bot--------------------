"""Проверки доступа и подписки на канал."""

from __future__ import annotations

import logging

from aiogram import Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramAPIError

logger = logging.getLogger(__name__)


async def is_subscribed(bot: Bot, channel_id: str | int, user_id: int) -> bool:
    """Проверяет подписку пользователя на канал через `get_chat_member`.

    Возвращает `True`, если пользователь состоит в канале (member/administrator/creator).
    При ошибках Telegram API или некорректных данных возвращает `False` и пишет в лог.
    """

    try:
        chat_member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    except TelegramAPIError:
        logger.exception(
            "Telegram API error while checking subscription: channel_id=%r user_id=%s",
            channel_id,
            user_id,
        )
        return False
    except Exception:
        logger.exception(
            "Unexpected error while checking subscription: channel_id=%r user_id=%s",
            channel_id,
            user_id,
        )
        return False

    status = chat_member.status
    is_member = status in {
        ChatMemberStatus.MEMBER,
        ChatMemberStatus.ADMINISTRATOR,
        ChatMemberStatus.CREATOR,
    }

    logger.info(
        "Subscription checked: channel_id=%r user_id=%s status=%s subscribed=%s",
        channel_id,
        user_id,
        status,
        is_member,
    )
    return is_member

