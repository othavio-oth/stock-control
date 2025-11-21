"""add created_at to tickets

Revision ID: d5e3c0cf4c21
Revises: ba9a4d7f3f2e
Create Date: 2025-12-01 00:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "d5e3c0cf4c21"
down_revision: Union[str, None] = "ba9a4d7f3f2e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column(inspector: sa.Inspector, table: str, column: str) -> bool:
    return any(col.get("name") == column for col in inspector.get_columns(table))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_column(inspector, "tickets", "created_at"):
        op.add_column(
            "tickets",
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_column(inspector, "tickets", "created_at"):
        op.drop_column("tickets", "created_at")
