"""Интеграционные тесты для API записей ежедневника."""

from datetime import time

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models.entry import EntryModel


@pytest.mark.asyncio
async def test_create_entry(client: AsyncClient) -> None:
    """Тест создания новой записи."""
    entry_data = {
        "title": "Важная встреча",
        "content": "Обсуждение проекта с командой",
        "event_time": "15:30:00"
    }

    response = await client.post("/api/v1/entries/", json=entry_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == entry_data["title"]
    assert data["content"] == entry_data["content"]
    assert data["event_time"] == "15:30:00"
    assert data["is_completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_entry_without_content(client: AsyncClient) -> None:
    """Тест создания записи без содержимого."""
    entry_data = {
        "title": "Краткая заметка",
        "event_time": "09:00:00"
    }

    response = await client.post("/api/v1/entries/", json=entry_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == entry_data["title"]
    assert data["content"] is None
    assert data["event_time"] == "09:00:00"


@pytest.mark.asyncio
async def test_get_entry(client: AsyncClient, db_session: AsyncSession) -> None:
    """Тест получения записи по ID."""
    entry = EntryModel(
        title="Тестовая запись",
        content="Тестовое содержимое",
        event_time=time(12, 0, 0)
    )
    db_session.add(entry)
    await db_session.commit()
    await db_session.refresh(entry)

    response = await client.get(f"/api/v1/entries/{entry.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == entry.id
    assert data["title"] == "Тестовая запись"
    assert data["content"] == "Тестовое содержимое"
    assert data["event_time"] == "12:00:00"


@pytest.mark.asyncio
async def test_get_entry_not_found(client: AsyncClient) -> None:
    """Тест получения несуществующей записи."""
    response = await client.get("/api/v1/entries/99999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Запись не найдена."


@pytest.mark.asyncio
async def test_list_entries_pagination(
    client: AsyncClient,
    db_session: AsyncSession
) -> None:
    """Тест пагинации списка записей."""
    for i in range(5):
        entry = EntryModel(
            title=f"Запись {i + 1}",
            content=f"Содержимое {i + 1}",
            event_time=time(10 + i, 0, 0)  # 10:00, 11:00, 12:00, 13:00, 14:00
        )
        db_session.add(entry)
    await db_session.commit()

    response = await client.get("/api/v1/entries/?skip=0&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Запись 1"
    assert data[1]["title"] == "Запись 2"

    response = await client.get("/api/v1/entries/?skip=2&limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Запись 3"
    assert data[1]["title"] == "Запись 4"


@pytest.mark.asyncio
async def test_filter_entries_by_completed(
    client: AsyncClient,
    db_session: AsyncSession
) -> None:
    """Тест фильтрации записей по статусу выполнения."""
    completed_entry = EntryModel(
        title="Выполненная задача",
        content="Уже сделано",
        event_time=time(10, 0, 0),
        is_completed=True
    )
    not_completed_entry = EntryModel(
        title="Невыполненная задача",
        content="Ещё нужно сделать",
        event_time=time(11, 0, 0),
        is_completed=False
    )
    db_session.add_all([completed_entry, not_completed_entry])
    await db_session.commit()

    response = await client.get("/api/v1/entries/?completed_only=true")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Выполненная задача"
    assert data[0]["is_completed"] is True

    response = await client.get("/api/v1/entries/?completed_only=false")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Невыполненная задача"
    assert data[0]["is_completed"] is False


@pytest.mark.asyncio
async def test_update_entry(client: AsyncClient, db_session: AsyncSession) -> None:
    """Тест обновления записи."""
    entry = EntryModel(
        title="Старый заголовок",
        content="Старое содержимое",
        event_time=time(9, 0, 0)
    )
    db_session.add(entry)
    await db_session.commit()
    await db_session.refresh(entry)

    update_data = {
        "title": "Новый заголовок",
        "content": "Новое содержимое",
        "event_time": "18:30:00"
    }

    response = await client.put(
        f"/api/v1/entries/{entry.id}",
        json=update_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["content"] == update_data["content"]
    assert data["event_time"] == "18:30:00"
    assert data["id"] == entry.id


@pytest.mark.asyncio
async def test_mark_entry_completed(
    client: AsyncClient,
    db_session: AsyncSession
) -> None:
    """Тест отметки записи как выполненной."""
    entry = EntryModel(
        title="Задача",
        content="Нужно сделать",
        event_time=time(14, 0, 0),
        is_completed=False
    )
    db_session.add(entry)
    await db_session.commit()
    await db_session.refresh(entry)

    response = await client.post(f"/api/v1/entries/{entry.id}/complete")

    assert response.status_code == 200
    data = response.json()
    assert data["is_completed"] is True

    await db_session.refresh(entry)
    assert entry.is_completed is True


@pytest.mark.asyncio
async def test_delete_entry(client: AsyncClient, db_session: AsyncSession) -> None:
    """Тест удаления записи."""
    entry = EntryModel(
        title="Удаляемая запись",
        content="Будет удалена",
        event_time=time(16, 0, 0)
    )
    db_session.add(entry)
    await db_session.commit()
    await db_session.refresh(entry)

    response = await client.delete(f"/api/v1/entries/{entry.id}")

    assert response.status_code == 200
    assert response.json() == {"detail": "Запись успешно удалена."}

    get_response = await client.get(f"/api/v1/entries/{entry.id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_entries_ordering_by_event_time(
    client: AsyncClient,
    db_session: AsyncSession
) -> None:
    """Тест сортировки записей по времени события."""
    entries = [
        EntryModel(title="Вечер", event_time=time(20, 0, 0)),
        EntryModel(title="Утро", event_time=time(8, 0, 0)),
        EntryModel(title="День", event_time=time(14, 0, 0)),
    ]
    db_session.add_all(entries)
    await db_session.commit()

    response = await client.get("/api/v1/entries/")

    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == "Утро"
    assert data[1]["title"] == "День"
    assert data[2]["title"] == "Вечер"
