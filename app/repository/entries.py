"""Репозиторий для работы с записями ежедневника."""

from datetime import time
from typing import Optional, Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.entry import EntryModel
from app.repository.base import BaseRepository


class EntriesRepository(BaseRepository[EntryModel]):
    """Класс репозитория для работы с записями ежедневника."""

    def __init__(self, session: AsyncSession) -> None:
        """Инициализирует репозиторий записей.

        Args:
            session: Асинхронная сессия базы данных.
        """
        # Теперь type ignore не нужен, так как мы правильно типизировали BaseRepository
        super().__init__(session=session, model=EntryModel)

    async def create_entry(
        self,
        title: str,
        content: str | None,
        event_time: time,
    ) -> EntryModel:
        """Создаёт новую запись ежедневника.

        Args:
            title: Краткое описание записи.
            content: Подробное описание записи.
            event_time: Время события.

        Returns:
            EntryModel: Созданная модель записи.
        """
        entry = EntryModel(
            title=title,
            content=content,
            event_time=event_time,
        )
        # Используем новый базовый метод add
        return await self.add(entry)

    async def update_entry(
        self,
        entry_id: int,
        title: str | None,
        content: str | None,
        event_time: time | None,
    ) -> EntryModel | None:
        """Обновляет существующую запись ежедневника.

        Args:
            entry_id: ID обновляемой записи.
            title: Новое краткое описание.
            content: Новое подробное описание.
            event_time: Новое время события.

        Returns:
            Optional[EntryModel]: Обновлённая запись или None, если запись не найдена.
        """
        values: dict[str, object] = {}
        if title is not None:
            values["title"] = title
        if content is not None:
            values["content"] = content
        if event_time is not None:
            values["event_time"] = event_time

        if not values:
            return await self.get_by_id(entry_id)

        stmt = (
            update(EntryModel)
            .where(EntryModel.id == entry_id)
            .values(**values)
            .returning(EntryModel)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_entry(self, entry_id: int) -> bool:
        """Удаляет запись ежедневника.

        Args:
            entry_id: ID записи для удаления.

        Returns:
            bool: True если запись была удалена, False если запись не найдена.
        """
        entry = await self.get_by_id(entry_id)
        if entry is None:
            return False

        await self._session.delete(entry)
        return True

    async def list_entries(
        self,
        skip: int = 0,
        limit: int = 100,
        completed_only: Optional[bool] = None,  # Добавлен параметр фильтрации
    ) -> Sequence[EntryModel]:
        """Возвращает список записей ежедневника с пагинацией и фильтрацией.

        Args:
            skip: Количество записей для пропуска.
            limit: Максимальное количество записей для возврата.
            completed_only: Если True - только выполненные,
                          если False - только невыполненные,
                          если None - все записи.

        Returns:
            Sequence[EntryModel]: Список записей, отсортированных по времени события.
        """
        query = select(EntryModel)

        if completed_only is not None:
            query = query.where(EntryModel.is_completed == completed_only)

        query = query.order_by(EntryModel.event_time).offset(skip).limit(limit)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def mark_completed(self, entry_id: int) -> EntryModel | None:
        """Помечает запись как отработанную.

        Args:
            entry_id: ID записи.

        Returns:
            Optional[EntryModel]: Обновлённая запись или None, если не найдена.
        """
        stmt = (
            update(EntryModel)
            .where(EntryModel.id == entry_id)
            .values(is_completed=True)
            .returning(EntryModel)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
