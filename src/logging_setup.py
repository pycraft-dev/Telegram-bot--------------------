"""Настройка логирования приложения."""

from __future__ import annotations

import logging
import os


def setup_logging() -> None:
    """Настраивает базовое логирование для приложения."""

    level_raw = os.getenv("LOG_LEVEL", "INFO").strip().upper() or "INFO"
    level = getattr(logging, level_raw, logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

