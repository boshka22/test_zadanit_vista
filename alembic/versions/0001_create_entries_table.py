"""Создание таблицы записей ежедневника."""

from typing import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0001_create_entries_table"
down_revision: str | None = None
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    """Создаёт таблицу `entries`."""

    op.create_table(
        "entries",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("event_time", sa.Time(), nullable=False),
        sa.Column(
            "is_completed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
    )


def downgrade() -> None:
    """Удаляет таблицу `entries`."""

    op.drop_table("entries")

