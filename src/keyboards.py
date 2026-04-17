"""Клавиатуры бота (reply и inline)."""

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Главное меню с постоянными кнопками."""

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Подписаться")],
            [KeyboardButton(text="Проверить подписку")],
        ],
        resize_keyboard=True,
        selective=False,
        is_persistent=True,
    )


def channel_link_keyboard(channel_link: str) -> InlineKeyboardMarkup:
    """Inline-кнопка для перехода в канал."""

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Перейти на канал", url=channel_link)],
        ]
    )

