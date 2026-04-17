"""Конфигурация приложения и загрузка переменных окружения."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import find_dotenv, load_dotenv


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Конфигурация Telegram-бота из переменных окружения."""

    bot_token: str
    channel_id: str
    channel_link: str
    guide_path: Path


_CACHED_CONFIG: AppConfig | None = None


def _require_env(name: str) -> str:
    """Возвращает обязательную переменную окружения или выбрасывает исключение."""

    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"Не задана обязательная переменная окружения: {name}")
    return value.strip()


def load_config() -> AppConfig:
    """Загружает конфиг из `.env` и кэширует результат."""

    global _CACHED_CONFIG
    if _CACHED_CONFIG is not None:
        return _CACHED_CONFIG

    cwd = Path.cwd()
    env_path = cwd / ".env"
    found_dotenv = find_dotenv(usecwd=True)

    if env_path.exists() and env_path.is_file():
        try:
            if env_path.stat().st_size == 0:
                raise RuntimeError(
                    "Файл .env найден, но он пустой (0 байт). "
                    "Сохраните .env на диск (UTF-8) и повторите запуск."
                )
        except OSError:
            pass

    # Пытаемся загрузить через python-dotenv. На Windows .env часто бывает сохранён в UTF-16.
    load_dotenv(dotenv_path=found_dotenv or None, override=False)

    bot_token = _require_env("BOT_TOKEN")
    channel_id = _require_env("CHANNEL_ID")
    channel_link = _require_env("CHANNEL_LINK")
    guide_path_raw = os.getenv("GUIDE_PATH", "src/guide.pdf").strip() or "src/guide.pdf"

    project_root = Path(__file__).resolve().parents[1]
    guide_path = Path(guide_path_raw)
    if not guide_path.is_absolute():
        guide_path = (project_root / guide_path).resolve()

    _CACHED_CONFIG = AppConfig(
        bot_token=bot_token,
        channel_id=channel_id,
        channel_link=channel_link,
        guide_path=guide_path,
    )
    return _CACHED_CONFIG

