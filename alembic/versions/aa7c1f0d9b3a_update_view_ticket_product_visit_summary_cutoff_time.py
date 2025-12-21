"""update view ticket_product_visit_summary cutoff to start of day when created_at missing

Revision ID: aa7c1f0d9b3a
Revises: f1a3d0e8c7ab
Create Date: 2025-12-02 02:00:00.000000
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aa7c1f0d9b3a"
down_revision: Union[str, None] = "f1a3d0e8c7ab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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
                    t.order_date::timestamp
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


def downgrade() -> None:
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
