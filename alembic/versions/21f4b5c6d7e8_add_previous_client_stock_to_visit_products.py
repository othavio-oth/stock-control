"""add previous_client_stock to inventory_visit_products

Revision ID: 21f4b5c6d7e8
Revises: fe2e4ac5c123
Create Date: 2025-12-09 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "21f4b5c6d7e8"
down_revision: Union[str, None] = "fe2e4ac5c123"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    return any(col.get("name") == column_name for col in inspector.get_columns(table_name))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_column(inspector, "inventory_visit_products", "previous_client_stock"):
        op.add_column(
            "inventory_visit_products",
            sa.Column("previous_client_stock", sa.Integer(), nullable=True),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_column(inspector, "inventory_visit_products", "previous_client_stock"):
        op.drop_column("inventory_visit_products", "previous_client_stock")
