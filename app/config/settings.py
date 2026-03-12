"""Модуль конфигурации приложения."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс настроек приложения.

    Значения могут переопределяться переменными окружения.
    """

    app_name: str = Field(default="Diary API", description="Название приложения.")
    debug: bool = Field(default=False, description="Флаг режима отладки.")

    database_url: str = Field(
        ...,
        description=(
            "DSN-строка подключения к PostgreSQL "
            "(например 'postgresql+asyncpg://user:pass@db:5432/db')."
        ),
    )

    class Config:
        """Конфигурация pydantic-settings."""

        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Возвращает кэшированный экземпляр настроек.

    Returns:
        Settings: объект настроек приложения.
    """

    return Settings()  # type: ignore[call-arg]
