from datetime import date, datetime
from operator import or_
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.stockMovement import ClientLossHistory, ClientSalesHistory, InventoryVisit, InventoryVisitProduct

from sqlalchemy.orm import joinedload

from app.models.tickets import CostCenter, Ticket, TicketProduct

def search_tickets_any( search_term: str,page:int,db: Session):
    page_size = 20
    offset = (page - 1) * page_size
    base_query = (
        db.query(Ticket)
          .options(
              joinedload(Ticket.products).joinedload(TicketProduct.product),
              joinedload(Ticket.inventory_visits)
              .joinedload(InventoryVisit.products)
              .joinedload(InventoryVisitProduct.product),
              joinedload(Ticket.inventory_visits).joinedload(InventoryVisit.cost_center),
          )  # <-- aqui
          .join(CostCenter)
          .filter(
              or_(
                  Ticket.id == int(search_term) if search_term.isdigit() else False,
                  Ticket.name.ilike(f"%{search_term}%"),
                  CostCenter.name.ilike(f"%{search_term}%"),
              )
          )
    )
    total = base_query.count()
    total_pages = (total + page_size - 1) // page_size

    tickets = base_query.offset(offset).limit(page_size).all()
    return {
    "items": tickets,
    "from django.utils.translation import ugettext_lazy as _": total,
    "page": page,
    "page_size": page_size,
    "total_pages": total_pages
    }

def recalculate_daily_visit_history(
    db: Session,
    *,
    cost_center_id: int,
    date_product_map: dict[date, set[int]],
) -> None:
    """
    Rebuilds the per-day sales/loss history for the provided products based on visit snapshots.
    """
    if not date_product_map:
        return

    for visit_date, product_ids in date_product_map.items():
        if visit_date is None or not product_ids:
            continue
        normalized_ids = sorted({int(pid) for pid in product_ids if pid is not None})
        if not normalized_ids:
            continue

        for product_id in normalized_ids:
            totals = (
                db.query(
                    func.coalesce(func.sum(InventoryVisitProduct.sales_quantity), 0).label("sales_total"),
                    func.coalesce(func.sum(InventoryVisitProduct.loss_quantity), 0).label("loss_total"),
                    func.max(InventoryVisit.visited_at).label("observed_at"),
                )
                .join(InventoryVisit, InventoryVisit.id == InventoryVisitProduct.inventory_visit_id)
                .filter(
                    InventoryVisit.cost_center_id == cost_center_id,
                    InventoryVisitProduct.product_id == product_id,
                    func.date(InventoryVisit.visited_at) == visit_date,
                )
                .first()
            )
            sales_total = int(totals.sales_total or 0) if totals else 0
            loss_total = int(totals.loss_total or 0) if totals else 0
            observed_at = totals.observed_at if totals else None

            set_client_sales_for_day(
                db,
                cost_center_id=cost_center_id,
                product_id=product_id,
                day=visit_date,
                total=sales_total,
                observed_at=observed_at,
            )
            set_client_loss_for_day(
                db,
                cost_center_id=cost_center_id,
                product_id=product_id,
                day=visit_date,
                total=loss_total,
                observed_at=observed_at,
            )


def set_client_sales_for_day(
    db: Session,
    *,
    cost_center_id: int,
    product_id: int,
    day: date,
    total: int,
    observed_at: Optional[datetime],
) -> None:
    record = (
        db.query(ClientSalesHistory)
        .filter_by(cost_center_id=cost_center_id, product_id=product_id, date=day)
        .first()
    )
    timestamp = observed_at or datetime.combine(day, datetime.min.time())

    if not record:
        record = ClientSalesHistory(
            cost_center_id=cost_center_id,
            product_id=product_id,
            date=day,
            sold_quantity=0,
        )
        db.add(record)
    record.sold_quantity = total
    record.observed_at = timestamp


def set_client_loss_for_day(
    db: Session,
    *,
    cost_center_id: int,
    product_id: int,
    day: date,
    total: int,
    observed_at: Optional[datetime],
) -> None:
    record = (
        db.query(ClientLossHistory)
        .filter_by(cost_center_id=cost_center_id, product_id=product_id, date=day)
        .first()
    )
    timestamp = observed_at or datetime.combine(day, datetime.min.time())

    if not record:
        record = ClientLossHistory(
            cost_center_id=cost_center_id,
            product_id=product_id,
            date=day,
            lost_quantity=0,
        )
        db.add(record)
    record.lost_quantity = total
    record.observed_at = timestamp
