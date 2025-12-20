"""add filtered column indexes

Revision ID: 3f2b1c9d7a10
Revises: a6653efb210a
Create Date: 2025-09-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f2b1c9d7a10"
down_revision: Union[str, None] = "a6653efb210a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # tickets: consultas por cost_center_id, status='approved', order_date < ... ORDER BY order_date DESC
    # Partial index para approved, com ordenação em order_date DESC
    op.create_index(
        "ix_tickets_cc_approved_orderdate",
        "tickets",
        ["cost_center_id", sa.text("order_date DESC")],
        unique=False,
        postgresql_where=sa.text("status = 'approved'"),
    )

    # ticket_products: filtros por ticket_id e product_id; e joins por product_id
    op.create_index(
        "ix_ticket_products_ticket_product",
        "ticket_products",
        ["ticket_id", "product_id"],
        unique=False,
    )
    op.create_index(
        "ix_ticket_products_product_id",
        "ticket_products",
        ["product_id"],
        unique=False,
    )

    # client_stock: consultas por (cost_center_id, product_id)
    op.create_index(
        "ix_client_stock_cc_product",
        "client_stock",
        ["cost_center_id", "product_id"],
        unique=False,
    )

    # client_loss_history: consultas por (cost_center_id, product_id) e intervalo de data
    op.create_index(
        "ix_client_loss_cc_product_date",
        "client_loss_history",
        ["cost_center_id", "product_id", "date"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_client_loss_cc_product_date", table_name="client_loss_history")
    op.drop_index("ix_client_stock_cc_product", table_name="client_stock")
    op.drop_index("ix_ticket_products_product_id", table_name="ticket_products")
    op.drop_index("ix_ticket_products_ticket_product", table_name="ticket_products")
    op.drop_index("ix_tickets_cc_approved_orderdate", table_name="tickets")

