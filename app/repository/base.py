"""Базовые классы репозиториев."""

from typing import Generic, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import AnyModel

ModelType = TypeVar("ModelType", bound=AnyModel)


class BaseRepository(Generic[ModelType]):
    """Базовый репозиторий для работы с моделями SQLAlchemy.

    Generic[ModelType] позволяет точно типизировать все методы,
    которые будут возвращать конкретную модель.
    """

    def __init__(self, session: AsyncSession, model: type[ModelType]) -> None:
        """Инициализирует репозиторий.

        Args:
            session: Асинхронная сессия базы данных.
            model: Класс модели SQLAlchemy (не экземпляр!).
        """
        self._session = session
        self._model = model

    async def get_by_id(self, obj_id: int) -> ModelType | None:
        """Возвращает объект по его идентификатору.

        Args:
            obj_id: Уникальный идентификатор объекта.

        Returns:
            Optional[ModelType]: Найденный объект или None.
        """
        return await self._session.get(self._model, obj_id)

    async def list_all(self) -> Sequence[ModelType]:
        """Возвращает список всех объектов.

        Returns:
            Sequence[ModelType]: Список объектов.
        """
        query = select(self._model)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def add(self, model: ModelType) -> ModelType:
        """Добавляет новую модель в сессию.

        Args:
            model: Экземпляр модели для добавления.

        Returns:
            ModelType: Добавленная модель.
        """
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(model)
        return model

    async def delete(self, model: ModelType) -> None:
        """Удаляет модель из сессии.

        Args:
            model: Экземпляр модели для удаления.
        """
        await self._session.delete(model)
