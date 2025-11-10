"""add inventory_visit_products table

Revision ID: d1b67f1840a3
Revises: c5499c9bca54
Create Date: 2025-11-30 01:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d1b67f1840a3"
down_revision: Union[str, None] = "c5499c9bca54"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("inventory_visit_products"):
        op.create_table(
            "inventory_visit_products",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("inventory_visit_id", sa.Integer(), nullable=False),
            sa.Column("product_id", sa.Integer(), nullable=False),
            sa.Column("stock_quantity", sa.Integer(), nullable=False),
            sa.Column("sales_quantity", sa.Integer(), nullable=False, server_default=sa.text("0")),
            sa.Column("loss_quantity", sa.Integer(), nullable=False, server_default=sa.text("0")),
            sa.ForeignKeyConstraint(
                ["inventory_visit_id"],
                ["inventory_visits.id"],
                name="fk_visit_product_visit",
                ondelete="CASCADE",
            ),
            sa.ForeignKeyConstraint(
                ["product_id"],
                ["products.id"],
                name="fk_visit_product_product",
            ),
        )
        op.create_unique_constraint(
            "uq_visit_product_visit_product",
            "inventory_visit_products",
            ["inventory_visit_id", "product_id"],
        )


def downgrade() -> None:
    op.drop_constraint("uq_visit_product_visit_product", "inventory_visit_products", type_="unique")
    op.drop_table("inventory_visit_products")
