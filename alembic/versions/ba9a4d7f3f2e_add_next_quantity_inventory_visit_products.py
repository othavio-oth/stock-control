"""add next_quantity to inventory_visit_products

Revision ID: ba9a4d7f3f2e
Revises: 9f3eee1b51f9
Create Date: 2025-12-01 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "ba9a4d7f3f2e"
down_revision: Union[str, None] = "9f3eee1b51f9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    columns = inspector.get_columns(table_name)
    return any(col.get("name") == column_name for col in columns)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_column(inspector, "inventory_visit_products", "next_quantity"):
        op.add_column(
            "inventory_visit_products",
            sa.Column("next_quantity", sa.Integer(), nullable=True),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_column(inspector, "inventory_visit_products", "next_quantity"):
        op.drop_column("inventory_visit_products", "next_quantity")
