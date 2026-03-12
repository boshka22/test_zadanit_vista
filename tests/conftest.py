"""Фикстуры для интеграционных тестов."""
# flake8: noqa: E402

import asyncio
import os
from typing import AsyncGenerator, Generator

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["DEBUG"] = "True"

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import create_app
from app.config.settings import Settings
from app.database.base import Base
from app.database.session import get_db_session

test_app = create_app()


class TestSettings(Settings):
    """Тестовые настройки."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def get_test_settings():
    """Возвращает тестовые настройки."""
    return TestSettings()


import app.config.settings
app.config.settings.get_settings = get_test_settings


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Создаёт event loop для сессии тестов."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Создаёт тестовую сессию БД с чистой схемой."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Создаёт тестовый HTTP клиент с переопределённой зависимостью БД."""

    async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    test_app.dependency_overrides[get_db_session] = override_get_db_session

    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac

    test_app.dependency_overrides.clear()
