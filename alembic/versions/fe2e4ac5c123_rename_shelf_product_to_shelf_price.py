"""rename shelf_product column to shelf_price

Revision ID: fe2e4ac5c123
Revises: c4d3b2a1d5e6
Create Date: 2025-12-08 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "fe2e4ac5c123"
down_revision: Union[str, None] = "c4d3b2a1d5e6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    return any(col.get("name") == column_name for col in inspector.get_columns(table_name))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    has_shelf_price = _has_column(inspector, "inventory_visit_products", "shelf_price")
    has_shelf_product = _has_column(inspector, "inventory_visit_products", "shelf_product")

    if not has_shelf_price and has_shelf_product:
        op.alter_column(
            "inventory_visit_products",
            "shelf_product",
            new_column_name="shelf_price",
        )
    elif not has_shelf_price and not has_shelf_product:
        op.add_column(
            "inventory_visit_products",
            sa.Column("shelf_price", sa.Numeric(precision=10, scale=2), nullable=True),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    has_shelf_price = _has_column(inspector, "inventory_visit_products", "shelf_price")
    has_shelf_product = _has_column(inspector, "inventory_visit_products", "shelf_product")

    if has_shelf_price and not has_shelf_product:
        op.alter_column(
            "inventory_visit_products",
            "shelf_price",
            new_column_name="shelf_product",
        )
