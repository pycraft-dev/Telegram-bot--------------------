"""Регистрация роутеров хендлеров."""

from aiogram import Router

from src.handlers.start import router as start_router
from src.handlers.subscription import router as subscription_router


def build_root_router() -> Router:
    """Собирает корневой роутер приложения."""

    router = Router()
    router.include_router(start_router)
    router.include_router(subscription_router)
    return router

