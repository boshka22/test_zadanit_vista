"""Маршруты для работы с записями ежедневника."""

from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query, status

from app.schemas.entries import EntryCreate, EntryRead, EntryUpdate
from app.services.entries import EntriesService, get_entries_service

router = APIRouter()


@router.post(
    "/",
    response_model=EntryRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать запись",
    description=(
        "Создаёт новую запись в ежедневнике с указанным заголовком, "
        "содержимым и временем события."
    ),
    responses={
        201: {"description": "Запись успешно создана"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def create_entry(
    entry_in: EntryCreate,
    service: EntriesService = Depends(get_entries_service),
) -> EntryRead:
    """Создаёт новую запись в ежедневнике.

    Args:
        entry_in: Данные для создания записи.
        service: Сервис для работы с записями.

    Returns:
        EntryRead: Созданная запись.
    """
    return await service.create_entry(entry_in=entry_in)


@router.get(
    "/{entry_id}",
    response_model=EntryRead,
    summary="Получить запись по ID",
    description=(
        "Возвращает детальную информацию о конкретной записи ежедневника."
    ),
    responses={
        200: {"description": "Запись найдена"},
        404: {"description": "Запись не найдена"},
        422: {"description": "Некорректный ID"},
    },
)
async def get_entry(
    entry_id: int = Path(
        ..., gt=0, description=(
            "ID существующей записи (целое положительное число)."
        )
    ),
    service: EntriesService = Depends(get_entries_service),
) -> EntryRead:
    """Возвращает запись по идентификатору.

    Args:
        entry_id: ID записи.
        service: Сервис для работы с записями.

    Returns:
        EntryRead: Найденная запись.
    """
    return await service.get_entry(entry_id=entry_id)


@router.get(
    "/",
    response_model=List[EntryRead],
    summary="Получить список записей",
    description=(
        "Возвращает список всех записей ежедневника с поддержкой пагинации.\n"
        "По умолчанию возвращаются первые 100 записей.\n"
        "Для навигации по страницам используйте параметры skip и limit."
    ),
    responses={
        200: {"description": "Список записей успешно получен"},
        422: {"description": "Некорректные параметры пагинации"},
    },
)
async def list_entries(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(
        100, ge=1, le=1000, description="Максимальное количество записей"
    ),
    completed_only: Optional[bool] = Query(
        None,
        description=(
            "Фильтр по статусу выполнения: true - выполненные, "
            "false - невыполненные, null - все"
        ),
    ),
    service: EntriesService = Depends(get_entries_service),
) -> List[EntryRead]:
    """Возвращает список записей ежедневника с поддержкой пагинации и фильтрации.

    Примеры:
        - GET /entries/?completed_only=true - только выполненные записи
        - GET /entries/?completed_only=false - только невыполненные записи
        - GET /entries/ - все записи (без фильтрации)
        - GET /entries/?skip=20&limit=10&completed_only=true
    """
    return await service.list_entries(
        skip=skip,
        limit=limit,
        completed_only=completed_only,
    )


@router.put(
    "/{entry_id}",
    response_model=EntryRead,
    summary="Обновить запись",
    description=(
        "Обновляет существующую запись ежедневника. "
        "Можно обновить одно или несколько полей."
    ),
    responses={
        200: {"description": "Запись успешно обновлена"},
        404: {"description": "Запись не найдена"},
        422: {"description": "Ошибка валидации данных"},
    },
)
async def update_entry(
    entry_in: EntryUpdate,
    entry_id: int = Path(
        ..., gt=0, description=(
            "ID существующей записи (целое положительное число)."
        )
    ),
    service: EntriesService = Depends(get_entries_service),
) -> EntryRead:
    """Обновляет содержимое записи.

    Args:
        entry_in: Новые данные записи.
        entry_id: ID записи для обновления.
        service: Сервис для работы с записями.

    Returns:
        EntryRead: Обновлённая запись.
    """
    return await service.update_entry(entry_id=entry_id, entry_in=entry_in)


@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_200_OK,
    summary="Удалить запись",
    description=(
        "Удаляет запись из ежедневника по указанному ID."
    ),
    responses={
        200: {"description": "Запись успешно удалена"},
        404: {"description": "Запись не найдена"},
        422: {"description": "Некорректный ID"},
    },
)
async def delete_entry(
    entry_id: int = Path(
        ..., gt=0, description=(
            "ID существующей записи (целое положительное число)."
        )
    ),
    service: EntriesService = Depends(get_entries_service),
) -> dict[str, str]:
    """Удаляет запись ежедневника.

    Args:
        entry_id: ID записи для удаления.
        service: Сервис для работы с записями.

    Returns:
        dict[str, str]: Сообщение об успешном удалении.
    """
    await service.delete_entry(entry_id=entry_id)
    return {"detail": "Запись успешно удалена."}


@router.post(
    "/{entry_id}/complete",
    response_model=EntryRead,
    summary="Отметить запись как выполненную",
    description=(
        "Помечает указанную запись как отработанную (выполненную)."
    ),
    responses={
        200: {"description": "Запись отмечена как выполненная"},
        404: {"description": "Запись не найдена"},
        422: {"description": "Некорректный ID"},
    },
)
async def mark_entry_completed(
    entry_id: int = Path(
        ..., gt=0, description=(
            "ID существующей записи (целое положительное число)."
        )
    ),
    service: EntriesService = Depends(get_entries_service),
) -> EntryRead:
    """Помечает запись как отработанную.

    Args:
        entry_id: ID записи.
        service: Сервис для работы с записями.

    Returns:
        EntryRead: Обновлённая запись.
    """
    return await service.mark_completed(entry_id=entry_id)
