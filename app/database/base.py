"""Базовые объекты SQLAlchemy."""

from typing import Union

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс моделей SQLAlchemy."""


class BaseModelMixin(Base):
    """Миксин с базовыми полями моделей.

    Attributes:
        id: Уникальный идентификатор записи.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(  # type: ignore[assignment]
        primary_key=True,
        index=True,
    )


AnyModel = Union[Base, BaseModelMixin]
