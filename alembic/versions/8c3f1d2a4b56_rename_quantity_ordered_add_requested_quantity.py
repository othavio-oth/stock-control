"""rename quantity_ordered to sent_quantity and add requested_quantity

Revision ID: 8c3f1d2a4b56
Revises: 21f4b5c6d7e8
Create Date: 2025-12-09 00:30:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8c3f1d2a4b56"
down_revision: Union[str, None] = "21f4b5c6d7e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _has_column(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    return any(col.get("name") == column_name for col in inspector.get_columns(table_name))


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # Rename quantity_ordered -> sent_quantity on ticket_products
    if _has_column(inspector, "ticket_products", "quantity_ordered") and not _has_column(
        inspector, "ticket_products", "sent_quantity"
    ):
        op.alter_column(
            "ticket_products",
            "quantity_ordered",
            new_column_name="sent_quantity",
        )

    # Add requested_quantity to inventory_visit_products
    if not _has_column(inspector, "inventory_visit_products", "requested_quantity"):
        op.add_column(
            "inventory_visit_products",
            sa.Column("requested_quantity", sa.Integer(), nullable=True),
        )

    # Recreate ticket_product_visit_summary view with the new column name
    op.execute(
        """
        DROP VIEW IF EXISTS ticket_product_visit_summary;
        CREATE OR REPLACE VIEW ticket_product_visit_summary AS
        WITH cutoff AS (
            SELECT
                t.id AS ticket_id,
                t.cost_center_id,
                COALESCE(
                    t.created_at,
                    t.approved_at,
                    (t.order_date::timestamp + INTERVAL '1 day' - INTERVAL '1 second')
                ) AS cutoff_at
            FROM tickets t
        ),
        ranked AS (
            SELECT
                c.ticket_id,
                ivp.product_id,
                iv.visited_at,
                ivp.stock_quantity,
                ivp.loss_quantity,
                ivp.sales_quantity,
                tp.sent_quantity,
                ROW_NUMBER() OVER (
                    PARTITION BY c.ticket_id, ivp.product_id
                    ORDER BY iv.visited_at DESC, iv.id DESC
                ) AS rn
            FROM cutoff c
            JOIN inventory_visits iv
              ON iv.cost_center_id = c.cost_center_id
             AND iv.visited_at < c.cutoff_at
            JOIN inventory_visit_products ivp
              ON ivp.inventory_visit_id = iv.id
            LEFT JOIN ticket_products tp
              ON tp.ticket_id = iv.ticket_id
             AND tp.product_id = ivp.product_id
        )
        SELECT
            ticket_id,
            product_id,
            MAX(CASE WHEN rn = 1 THEN loss_quantity END)  AS loss_last,
            MAX(CASE WHEN rn = 2 THEN loss_quantity END)  AS loss_prev,
            MAX(CASE WHEN rn = 1 THEN sales_quantity END) AS sales_last,
            MAX(CASE WHEN rn = 2 THEN sales_quantity END) AS sales_prev,
            MAX(CASE WHEN rn = 1 THEN stock_quantity END) AS stock_last,
            MAX(CASE WHEN rn = 2 THEN stock_quantity END) AS stock_prev,
            MAX(CASE WHEN rn = 1 THEN sent_quantity END) AS order_last,
            MAX(CASE WHEN rn = 2 THEN sent_quantity END) AS order_prev,
            MAX(CASE WHEN rn = 2 THEN visited_at END) AS order_prev_date
        FROM ranked
        WHERE rn <= 2
        GROUP BY ticket_id, product_id;
        """
    )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if _has_column(inspector, "inventory_visit_products", "requested_quantity"):
        op.drop_column("inventory_visit_products", "requested_quantity")

    if _has_column(inspector, "ticket_products", "sent_quantity") and not _has_column(
        inspector, "ticket_products", "quantity_ordered"
    ):
        op.alter_column(
            "ticket_products",
            "sent_quantity",
            new_column_name="quantity_ordered",
        )

    # Restore view definition with the old column name
    op.execute(
        """
        DROP VIEW IF EXISTS ticket_product_visit_summary;
        CREATE OR REPLACE VIEW ticket_product_visit_summary AS
        WITH cutoff AS (
            SELECT
                t.id AS ticket_id,
                t.cost_center_id,
                COALESCE(
                    t.created_at,
                    t.approved_at,
                    (t.order_date::timestamp + INTERVAL '1 day' - INTERVAL '1 second')
                ) AS cutoff_at
            FROM tickets t
        ),
        ranked AS (
            SELECT
                c.ticket_id,
                ivp.product_id,
                iv.visited_at,
                ivp.stock_quantity,
                ivp.loss_quantity,
                ivp.sales_quantity,
                tp.quantity_ordered,
                ROW_NUMBER() OVER (
                    PARTITION BY c.ticket_id, ivp.product_id
                    ORDER BY iv.visited_at DESC, iv.id DESC
                ) AS rn
            FROM cutoff c
            JOIN inventory_visits iv
              ON iv.cost_center_id = c.cost_center_id
             AND iv.visited_at < c.cutoff_at
            JOIN inventory_visit_products ivp
              ON ivp.inventory_visit_id = iv.id
            LEFT JOIN ticket_products tp
              ON tp.ticket_id = iv.ticket_id
             AND tp.product_id = ivp.product_id
        )
        SELECT
            ticket_id,
            product_id,
            MAX(CASE WHEN rn = 1 THEN loss_quantity END)  AS loss_last,
            MAX(CASE WHEN rn = 2 THEN loss_quantity END)  AS loss_prev,
            MAX(CASE WHEN rn = 1 THEN sales_quantity END) AS sales_last,
            MAX(CASE WHEN rn = 2 THEN sales_quantity END) AS sales_prev,
            MAX(CASE WHEN rn = 1 THEN stock_quantity END) AS stock_last,
            MAX(CASE WHEN rn = 2 THEN stock_quantity END) AS stock_prev,
            MAX(CASE WHEN rn = 1 THEN quantity_ordered END) AS order_last,
            MAX(CASE WHEN rn = 2 THEN quantity_ordered END) AS order_prev,
            MAX(CASE WHEN rn = 2 THEN visited_at END) AS order_prev_date
        FROM ranked
        WHERE rn <= 2
        GROUP BY ticket_id, product_id;
        """
    )
