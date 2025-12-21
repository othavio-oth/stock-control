"""add inventory visit entity

Revision ID: c5499c9bca54
Revises: 8901358fea1d
Create Date: 2025-11-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c5499c9bca54"
down_revision: Union[str, None] = "8901358fea1d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "inventory_visits",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("cost_center_id", sa.Integer(), nullable=False),
        sa.Column("ticket_id", sa.Integer(), nullable=True),
        sa.Column("recorded_by", sa.Integer(), nullable=True),
        sa.Column("visited_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("total_stock_quantity", sa.Integer(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["cost_center_id"], ["cost_centers.id"], name="fk_inventory_visit_cost_center"),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], name="fk_inventory_visit_ticket"),
        sa.ForeignKeyConstraint(["recorded_by"], ["users.id"], name="fk_inventory_visit_user"),
    )
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

    op.add_column(
        "stock_movements",
        sa.Column("inventory_visit_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        "fk_stock_movements_inventory_visit",
        "stock_movements",
        "inventory_visits",
        ["inventory_visit_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index(
        "ix_stock_movements_inventory_visit_id",
        "stock_movements",
        ["inventory_visit_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_stock_movements_inventory_visit_id", table_name="stock_movements")
    op.drop_constraint("fk_stock_movements_inventory_visit", "stock_movements", type_="foreignkey")
    op.drop_column("stock_movements", "inventory_visit_id")
    op.drop_constraint("uq_visit_product_visit_product", "inventory_visit_products", type_="unique")
    op.drop_table("inventory_visit_products")
    op.drop_table("inventory_visits")
