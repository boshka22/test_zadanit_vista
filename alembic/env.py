"""Alembic-настройка окружения для миграций."""

from __future__ import annotations

import asyncio
import os
import sys
from logging.config import fileConfig
from typing import Any

from alembic import context
from sqlalchemy import Connection, pool
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, async_engine_from_config

# Добавляем корень проекта в sys.path, чтобы можно было импортировать пакет `app`
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.config.settings import get_settings
from app.database.base import Base
from app.database.models import entry  # noqa: F401  # импорт для регистрации моделей

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _get_url() -> str:
    """Возвращает URL подключения к базе данных для Alembic.

    Returns:
        str: DSN-строка подключения к PostgreSQL.
    """

    settings = get_settings()
    return settings.database_url


def run_migrations_offline() -> None:
    """Запускает миграции в оффлайн-режиме."""

    url = _get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Выполняет миграции, используя переданное подключение.

    Args:
        connection: Синхронное подключение SQLAlchemy.
    """

    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запускает миграции в онлайн-режиме с использованием AsyncEngine."""

    configuration: dict[str, Any] = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = _get_url()

    connectable: AsyncEngine = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())

