"""Точка входа в приложение FastAPI для ежедневника."""

from fastapi import FastAPI

from app.api.v1.router import api_router


def create_app() -> FastAPI:
    """Создаёт и настраивает экземпляр FastAPI.

    Returns:
        FastAPI: сконфигурированное приложение.
    """

    app = FastAPI(
        title="Diary API",
        version="1.0.0",
        description="Приложение-ежедневник на основе FastAPI.",
    )

    app.include_router(api_router, prefix="/api/v1")
    return app


app = create_app()
