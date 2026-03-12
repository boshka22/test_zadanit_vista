"""Сервисный слой для работы с записями ежедневника."""

from typing import List, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db_session
from app.repository.entries import EntriesRepository
from app.schemas.entries import EntryCreate, EntryRead, EntryUpdate


class EntriesService:
    """Класс сервиса для работы с записями ежедневника."""

    def __init__(self, repo: EntriesRepository, session: AsyncSession) -> None:
        """Инициализирует сервис.

        Args:
            repo: Репозиторий записей.
            session: Асинхронная сессия базы данных.
        """

        self._repo = repo
        self._session = session

    async def create_entry(self, entry_in: EntryCreate) -> EntryRead:
        """Создаёт новую запись ежедневника.

        Args:
            entry_in: Данные для создания записи.

        Returns:
            EntryRead: Созданная запись.
        """

        entry = await self._repo.create_entry(
            title=entry_in.title,
            content=entry_in.content,
            event_time=entry_in.event_time,
        )
        await self._session.commit()
        return EntryRead.model_validate(entry)

    async def get_entry(self, entry_id: int) -> EntryRead:
        """Возвращает запись по ID.

        Args:
            entry_id: ID записи.

        Returns:
            EntryRead: Найденная запись.

        Raises:
            HTTPException: Если запись не найдена.
        """

        entry = await self._repo.get_by_id(entry_id)
        if entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запись не найдена.",
            )
        return EntryRead.model_validate(entry)

    async def list_entries(
        self,
        skip: int = 0,
        limit: int = 100,
        completed_only: Optional[bool] = None,
    ) -> List[EntryRead]:
        """Возвращает список записей ежедневника с пагинацией и фильтрацией.

        Args:
            skip: Количество записей для пропуска.
            limit: Максимальное количество записей для возврата.
            completed_only: Фильтр по статусу выполнения.

        Returns:
            list[EntryRead]: Список записей.
        """
        entries = await self._repo.list_entries(
            skip=skip,
            limit=limit,
            completed_only=completed_only,
        )
        return [EntryRead.model_validate(obj) for obj in entries]

    async def update_entry(self, entry_id: int, entry_in: EntryUpdate) -> EntryRead:
        """Обновляет существующую запись.

        Args:
            entry_id: ID записи.
            entry_in: Новые данные для записи.

        Returns:
            EntryRead: Обновлённая запись.

        Raises:
            HTTPException: Если запись не найдена.
        """

        entry = await self._repo.update_entry(
            entry_id=entry_id,
            title=entry_in.title,
            content=entry_in.content,
            event_time=entry_in.event_time,
        )
        if entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запись не найдена.",
            )
        await self._session.commit()
        return EntryRead.model_validate(entry)

    async def delete_entry(self, entry_id: int) -> None:
        """Удаляет запись ежедневника.

        Args:
            entry_id: ID записи.

        Raises:
            HTTPException: Если запись не найдена.
        """
        deleted = await self._repo.delete_entry(entry_id=entry_id)

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запись не найдена.",
            )

        await self._session.commit()

    async def mark_completed(self, entry_id: int) -> EntryRead:
        """Помечает запись как отработанную.

        Args:
            entry_id: ID записи.

        Returns:
            EntryRead: Обновлённая запись.

        Raises:
            HTTPException: Если запись не найдена.
        """

        entry = await self._repo.mark_completed(entry_id=entry_id)
        if entry is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запись не найдена.",
            )
        await self._session.commit()
        return EntryRead.model_validate(entry)


def get_entries_service(
    session: AsyncSession = Depends(get_db_session),
) -> EntriesService:
    """Провайдер зависимости сервиса записей для FastAPI.

    Args:
        session: Асинхронная сессия базы данных.

    Returns:
        EntriesService: Экземпляр сервиса записей.
    """

    repo = EntriesRepository(session=session)
    return EntriesService(repo=repo, session=session)
