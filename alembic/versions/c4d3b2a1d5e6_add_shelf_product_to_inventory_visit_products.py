"""add shelf_price to inventory_visit_products

Revision ID: c4d3b2a1d5e6
Revises: b1b4f71e0a2f
Create Date: 2025-12-07 00:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c4d3b2a1d5e6"
down_revision: Union[str, None] = "b1b4f71e0a2f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "inventory_visit_products",
        sa.Column("shelf_price", sa.Numeric(precision=10, scale=2), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("inventory_visit_products", "shelf_price")
