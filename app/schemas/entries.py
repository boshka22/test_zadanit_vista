"""Pydantic-схемы для работы с записями ежедневника."""

from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, Field


class EntryBase(BaseModel):
    """Базовая схема записи ежедневника."""

    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = Field(None, max_length=5000)
    event_time: time  # Pydantic сам примет "18:30" и "18:30:00"


class EntryCreate(EntryBase):
    pass


class EntryUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, max_length=5000)
    event_time: Optional[time] = None


class EntryRead(EntryBase):
    id: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
