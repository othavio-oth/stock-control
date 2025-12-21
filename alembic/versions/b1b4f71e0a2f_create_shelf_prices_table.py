"""create shelf_prices table

Revision ID: b1b4f71e0a2f
Revises: aa7c1f0d9b3a
Create Date: 2025-12-07 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b1b4f71e0a2f"
down_revision: Union[str, None] = "aa7c1f0d9b3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "shelf_prices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("retail_chain_id", sa.Integer(), nullable=True),
        sa.Column("cost_center_id", sa.Integer(), nullable=True),
        sa.Column("percentage_rate", sa.Numeric(precision=10, scale=4), nullable=False),
        sa.Column("start_date", sa.DateTime(), server_default=sa.func.now(), nullable=True),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.CheckConstraint(
            "(retail_chain_id IS NOT NULL AND cost_center_id IS NULL) OR (retail_chain_id IS NULL AND cost_center_id IS NOT NULL)",
            name="check_shelf_price_scope",
        ),
        sa.ForeignKeyConstraint(["cost_center_id"], ["cost_centers.id"]),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["retail_chain_id"], ["retail_chains.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("product_id", "retail_chain_id", "start_date", name="uix_shelf_price_chain_start"),
        sa.UniqueConstraint("product_id", "cost_center_id", "start_date", name="uix_shelf_price_cost_center_start"),
    )


def downgrade() -> None:
    op.drop_table("shelf_prices")
