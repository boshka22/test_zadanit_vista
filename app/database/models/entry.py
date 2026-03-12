"""SQLAlchemy-модель записи ежедневника."""

from datetime import datetime, time

from sqlalchemy import Boolean, DateTime, Time, func, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import BaseModelMixin


class EntryModel(BaseModelMixin):
    """Модель записи ежедневника."""

    __tablename__ = "entries"

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        doc="Краткое описание события.",
    )
    content: Mapped[str | None] = mapped_column(
        String(5000),
        nullable=True,
        doc="Подробное описание события.",
    )
    event_time: Mapped[time] = mapped_column(
        Time,
        nullable=False,
        doc="Время события (часы и минуты).",
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        doc="Флаг, показывающий, что запись отработана.",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc="Дата и время создания записи.",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        doc="Дата и время последнего обновления записи.",
    )
