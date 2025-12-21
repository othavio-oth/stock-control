from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_

from app.models.stockMovement import ClientLossHistory, ClientSalesHistory, InventoryVisit, InventoryVisitProduct
from app.models.tickets import TicketProduct
from app.schemas.tickets_schemas.inventory_visit_schema import ProductCycleBlock
from app.service.utils.date_utils import date_to_str


def build_cycle_block(visit_row) -> Optional[ProductCycleBlock]:
        if not visit_row:
            return None

        sales_value = None
        if hasattr(visit_row, "sales_quantity_history"):
            sales_value = int(visit_row.sales_quantity_history)
        elif hasattr(visit_row, "sales_quantity") and getattr(visit_row, "sales_quantity", None) is not None:
            sales_value = int(visit_row.sales_quantity)

        loss_value = None
        if hasattr(visit_row, "loss_quantity_history"):
            loss_value = int(visit_row.loss_quantity_history)
        elif getattr(visit_row, "loss_quantity", None) is not None:
            loss_value = int(visit_row.loss_quantity)

        return ProductCycleBlock(
            ticket_id=getattr(visit_row, "ticket_id", None),
            date=date_to_str(getattr(visit_row, "visited_at", None)),
            ordered=(
                int(visit_row.sent_quantity)
                if getattr(visit_row, "sent_quantity", None) is not None
                else None
            ),
            stock=int(visit_row.stock_quantity) if getattr(visit_row, "stock_quantity", None) is not None else None,
            loss=loss_value,
            sales=sales_value,
        )



def collect_visits_by_product(
        db: Session,
        *,
        cost_center_id: int,
        product_ids: List[int],
        allowed_ticket_ids: Optional[List[int]] = None,
    ) -> dict[int, list]:
        if not product_ids:
            return {}

        visit_rank = func.row_number().over(
            partition_by=InventoryVisitProduct.product_id,
            order_by=(InventoryVisit.visited_at.desc(), InventoryVisit.id.desc()),
        ).label("visit_rank")

        base_query = (
            db.query(
                InventoryVisitProduct.product_id.label("product_id"),
                InventoryVisit.ticket_id.label("ticket_id"),
                InventoryVisit.visited_at.label("visited_at"),
                InventoryVisitProduct.stock_quantity.label("stock_quantity"),
                InventoryVisitProduct.loss_quantity.label("loss_quantity"),
                InventoryVisitProduct.requested_quantity.label("requested_quantity"),
                InventoryVisitProduct.next_quantity.label("next_quantity"),
                InventoryVisitProduct.shelf_price.label("shelf_price"),
                func.coalesce(ClientSalesHistory.sold_quantity, 0).label("sales_quantity_history"),
                func.coalesce(ClientLossHistory.lost_quantity, 0).label("loss_quantity_history"),
                TicketProduct.sent_quantity.label("sent_quantity"),
                visit_rank,
            )
            .join(InventoryVisit, InventoryVisit.id == InventoryVisitProduct.inventory_visit_id)
            .join(
                TicketProduct,
                and_(
                    TicketProduct.ticket_id == InventoryVisit.ticket_id,
                    TicketProduct.product_id == InventoryVisitProduct.product_id,
                ),
            )
            .outerjoin(
                ClientSalesHistory,
                and_(
                    ClientSalesHistory.product_id == InventoryVisitProduct.product_id,
                    ClientSalesHistory.cost_center_id == InventoryVisit.cost_center_id,
                    ClientSalesHistory.date == func.date(InventoryVisit.visited_at),
                ),
            )
            .outerjoin(
                ClientLossHistory,
                and_(
                    ClientLossHistory.product_id == InventoryVisitProduct.product_id,
                    ClientLossHistory.cost_center_id == InventoryVisit.cost_center_id,
                    ClientLossHistory.date == func.date(InventoryVisit.visited_at),
                ),
            )
            .filter(
                InventoryVisit.cost_center_id == cost_center_id,
                InventoryVisitProduct.product_id.in_(product_ids),
                or_(
                    InventoryVisitProduct.stock_quantity.isnot(None),
                    InventoryVisitProduct.loss_quantity.isnot(None),
                    InventoryVisitProduct.sales_quantity.isnot(None),
                ),
            )
        )

        if allowed_ticket_ids:
            base_query = base_query.filter(InventoryVisit.ticket_id.in_(allowed_ticket_ids))

        visit_subquery = base_query.subquery()

        visit_rows = (
            db.query(visit_subquery)
            .filter(visit_subquery.c.visit_rank <= 3)
            .order_by(visit_subquery.c.product_id, visit_subquery.c.visit_rank)
            .all()
        )

        visits_by_product: dict[int, list] = {}
        for row in visit_rows:
            visits_by_product.setdefault(row.product_id, []).append(row)
        return visits_by_product
