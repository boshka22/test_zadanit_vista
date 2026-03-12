"""${message}"""

revision = ${repr(revision_id)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

from alembic import op  # noqa: E402
import sqlalchemy as sa  # noqa: E402


def upgrade() -> None:
    """Применяет миграцию."""

    pass


def downgrade() -> None:
    """Откатывает миграцию."""

    pass

