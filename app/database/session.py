"""Создание и управление подключением к базе данных."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.settings import get_settings


def get_engine() -> AsyncEngine:
    """Создаёт асинхронный движок SQLAlchemy.

    Returns:
        AsyncEngine: асинхронный движок для подключения к PostgreSQL.
    """

    settings = get_settings()
    return create_async_engine(str(settings.database_url), echo=settings.debug)


async_engine: AsyncEngine = get_engine()

AsyncSessionMaker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Зависимость FastAPI для предоставления асинхронной сессии БД.

    Yields:
        AsyncSession: сессия базы данных.
    """

    async with AsyncSessionMaker() as session:
        yield session
