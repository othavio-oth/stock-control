from datetime import datetime, timezone
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload
from starlette.status import HTTP_404_NOT_FOUND

from app.models.product import Product
from app.models.stockMovement import InventoryVisit, InventoryVisitProduct
from app.models.tickets import Ticket, TicketProduct
from app.repository.tickets.tickets_repository import get_ticket_by_id
from app.schemas.tickets_schemas.inventory_visit_schema import (
    CostCenterLatestVisitsResponse,
    CostCenterProductVisitsResponse,
    CostCenterVisitSnapshot,
    ProductCycleTimelineResponse,
    ProductVisitSnapshot,
    ReservationItem,
    ReservationTicketItem,
    ReservationsResponse,
    TicketCycleProductsResponse,
    TicketVisitSummaryItem,
    TicketVisitSummaryResponse,
    VisitProductSnapshot,
)
from app.service.utils.date_utils import date_to_str
from app.service.utils.ticket_utils import get_allowed_ticket_ids
from app.service.utils.visit_utils import build_cycle_block, collect_visits_by_product


class TicketReportingService:
    @staticmethod
    def get_ticket_cycle_products(db: Session, ticket_id: int) -> TicketCycleProductsResponse:
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket nuo encontrado")

        product_ids = list({tp.product_id for tp in ticket.products})
        visits_by_product = collect_visits_by_product(
            db,
            cost_center_id=ticket.cost_center_id,
            product_ids=product_ids,
            allowed_ticket_ids=get_allowed_ticket_ids(db, ticket),
        )
        seen_products: set[int] = set()
        products_payload: list[ProductCycleTimelineResponse] = []
        for tp in ticket.products:
            if tp.product_id in seen_products:
                continue
            seen_products.add(tp.product_id)

            visit_entries = visits_by_product.get(tp.product_id, [])

            current_block = build_cycle_block(visit_entries[0]) if len(visit_entries) > 0 else None
            previous_block = build_cycle_block(visit_entries[1]) if len(visit_entries) > 1 else None
            previous2_block = build_cycle_block(visit_entries[2]) if len(visit_entries) > 2 else None

            products_payload.append(
                ProductCycleTimelineResponse(
                    product_id=tp.product_id,
                    name=getattr(tp.product, "name", None),
                    custom_id=getattr(tp.product, "custom_id", None),
                    previous2=previous2_block,
                    previous=previous_block,
                    current=current_block,
                )
            )

        return TicketCycleProductsResponse(
            ticket_id=ticket.id,
            cost_center_id=ticket.cost_center_id,
            products=products_payload,
        )
        
    @staticmethod
    def get_cost_center_product_visits(
        db: Session,
        *,
        cost_center_id: int,
        product_ids: Optional[List[int]] = None,
    ) -> CostCenterProductVisitsResponse:
        if product_ids:
            filtered_ids = sorted({int(pid) for pid in product_ids})
        else:
            filtered_ids = [
                row.product_id
                for row in (
                    db.query(InventoryVisitProduct.product_id)
                    .join(InventoryVisit, InventoryVisit.id == InventoryVisitProduct.inventory_visit_id)
                    .filter(InventoryVisit.cost_center_id == cost_center_id)
                    .distinct()
                    .all()
                )
            ]

        if not filtered_ids:
            return CostCenterProductVisitsResponse(cost_center_id=cost_center_id, visits=[])

        products = (
            db.query(Product.id, Product.name, Product.custom_id)
            .filter(Product.id.in_(filtered_ids))
            .all()
        )
        product_meta = {
            row.id: {"name": row.name, "custom_id": row.custom_id}
            for row in products
        }
        if not product_meta:
            return CostCenterProductVisitsResponse(cost_center_id=cost_center_id, visits=[])

        visits_by_product = collect_visits_by_product(
            db,
            cost_center_id=cost_center_id,
            product_ids=list(product_meta.keys()),
        )

        visits_payload: list[ProductVisitSnapshot] = []
        for product_id, meta in product_meta.items():
            visit_entries = visits_by_product.get(product_id, [])
            for visit_row in visit_entries:
                visits_payload.append(
                    ProductVisitSnapshot(
                        product_id=product_id,
                        name=meta.get("name"),
                        custom_id=meta.get("custom_id"),
                        ticket_id=getattr(visit_row, "ticket_id", None),
                        visited_at=date_to_str(getattr(visit_row, "visited_at", None)),
                        quantity_ordered=(
                            int(visit_row.quantity_ordered)
                            if getattr(visit_row, "quantity_ordered", None) is not None
                            else None
                        ),
                        shelf_price=(
                            float(visit_row.shelf_price)
                            if getattr(visit_row, "shelf_price", None) is not None
                            else None
                        ),
                        stock_quantity=(
                            int(visit_row.stock_quantity)
                            if getattr(visit_row, "stock_quantity", None) is not None
                            else None
                        ),
                        loss_quantity=(
                            int(visit_row.loss_quantity)
                            if getattr(visit_row, "loss_quantity", None) is not None
                            else None
                        ),
                        next_qty=(
                            int(visit_row.next_quantity)
                            if getattr(visit_row, "next_quantity", None) is not None
                            else None
                        ),
                    )
                )

        return CostCenterProductVisitsResponse(
            cost_center_id=cost_center_id,
            visits=visits_payload,
        )

    @staticmethod
    def get_cost_center_latest_visits(
        db: Session,
        *,
        cost_center_id: int,
        limit: int = 2,
        ticket_id: Optional[int] = None,
    ) -> CostCenterLatestVisitsResponse:
        effective_limit = limit if isinstance(limit, int) and limit > 0 else 2
        base_query = (
            db.query(InventoryVisit)
            .options(
                joinedload(InventoryVisit.products).joinedload(InventoryVisitProduct.product),
            )
            .filter(InventoryVisit.cost_center_id == cost_center_id)
            .order_by(InventoryVisit.visited_at.desc(), InventoryVisit.id.desc())
        )

        visits: list[InventoryVisit] = []
        if ticket_id:
            visits_query = base_query.filter(
                InventoryVisit.ticket_id.isnot(None),
                InventoryVisit.ticket_id <= ticket_id,
            )
            if effective_limit > 0:
                visits_query = visits_query.limit(effective_limit)
            visits = visits_query.all()
        else:
            visits_query = base_query
            if effective_limit > 0:
                visits_query = visits_query.limit(effective_limit)
            visits = visits_query.all()

        if not visits:
            return CostCenterLatestVisitsResponse(cost_center_id=cost_center_id, visits=[])

        ticket_ids = {visit.ticket_id for visit in visits if visit.ticket_id}
        ticket_product_rows = (
            db.query(
                TicketProduct.ticket_id.label("ticket_id"),
                TicketProduct.product_id.label("product_id"),
                TicketProduct.quantity_ordered.label("quantity_ordered"),
            )
            .filter(TicketProduct.ticket_id.in_(ticket_ids))
            .all()
            if ticket_ids
            else []
        )
        quantity_map = {
            (row.ticket_id, row.product_id): int(row.quantity_ordered) if row.quantity_ordered is not None else None
            for row in ticket_product_rows
        }

        visit_payloads: list[CostCenterVisitSnapshot] = []
        for visit in visits:
            products_payload: list[VisitProductSnapshot] = []
            for product_entry in visit.products or []:
                products_payload.append(
                    VisitProductSnapshot(
                        product_id=product_entry.product_id,
                        name=getattr(product_entry.product, "name", None),
                        custom_id=getattr(product_entry.product, "custom_id", None),
                        quantity_ordered=quantity_map.get((visit.ticket_id, product_entry.product_id)),
                        stock_quantity=product_entry.stock_quantity,
                        loss_quantity=product_entry.loss_quantity,
                        shelf_price=float(product_entry.shelf_price) if product_entry.shelf_price is not None else None,
                        next_qty=product_entry.next_quantity,
                    )
                )

            visit_payloads.append(
                CostCenterVisitSnapshot(
                    visit_id=visit.id,
                    ticket_id=visit.ticket_id,
                    visited_at=date_to_str(visit.visited_at),
                    total_stock_quantity=visit.total_stock_quantity,
                    products=products_payload,
                )
            )

        return CostCenterLatestVisitsResponse(
            cost_center_id=cost_center_id,
            visits=visit_payloads,
        )

    @staticmethod
    def get_ticket_visit_summary(db: Session, ticket_id: int) -> TicketVisitSummaryResponse:
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Ticket nao encontrado.")

        cutoff_dt = None
        if getattr(ticket, "order_date", None):
            cutoff_dt = datetime.combine(ticket.order_date, datetime.max.time())
        elif getattr(ticket, "approved_at", None):
            cutoff_dt = ticket.approved_at
        elif getattr(ticket, "created_at", None):
            cutoff_dt = ticket.created_at
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Data de referencia do ticket nao encontrada.")

        # Normaliza cutoff para evitar comparações inconsistentes de timezone
        if cutoff_dt:
            if cutoff_dt.tzinfo is None:
                cutoff_dt = cutoff_dt.replace(tzinfo=timezone.utc)
            else:
                cutoff_dt = cutoff_dt.astimezone(timezone.utc)

        rows = db.execute(
            text(
                """
                WITH ranked AS (
                    SELECT
                        ivp.product_id,
                        iv.visited_at,
                        ivp.loss_quantity,
                        ivp.sales_quantity,
                        ivp.stock_quantity,
                        ivp.next_quantity,
                        tp.quantity_ordered,
                        ROW_NUMBER() OVER (
                            PARTITION BY ivp.product_id
                            ORDER BY iv.visited_at DESC, iv.id DESC
                        ) AS rn
                    FROM inventory_visits iv
                    JOIN inventory_visit_products ivp ON ivp.inventory_visit_id = iv.id
                    LEFT JOIN ticket_products tp
                        ON tp.ticket_id = iv.ticket_id
                        AND tp.product_id = ivp.product_id
                    WHERE iv.cost_center_id = :cost_center_id
                      AND iv.visited_at < :cutoff
                )
                SELECT
                    product_id,
                    MAX(CASE WHEN rn = 1 THEN loss_quantity END)  AS loss_last,
                    MAX(CASE WHEN rn = 2 THEN loss_quantity END)  AS loss_prev,
                    MAX(CASE WHEN rn = 1 THEN sales_quantity END) AS sales_last,
                    MAX(CASE WHEN rn = 2 THEN sales_quantity END) AS sales_prev,
                    MAX(CASE WHEN rn = 1 THEN stock_quantity END) AS stock_last,
                    MAX(CASE WHEN rn = 2 THEN stock_quantity END) AS stock_prev,
                    MAX(CASE WHEN rn = 1 THEN next_quantity END) AS next_qty,
                    MAX(CASE WHEN rn = 1 THEN quantity_ordered END) AS order_last,
                    MAX(CASE WHEN rn = 2 THEN quantity_ordered END) AS order_prev,
                    MAX(CASE WHEN rn = 2 THEN visited_at END) AS order_prev_date
                FROM ranked
                WHERE rn <= 2
                GROUP BY product_id
                ORDER BY product_id
                """
            ),
            {
                "ticket_id": ticket_id,
                "cost_center_id": ticket.cost_center_id,
                "cutoff": cutoff_dt,
            },
        ).fetchall()

        items = []
        approved_tickets = (
            db.query(Ticket)
            .filter(
                Ticket.cost_center_id == ticket.cost_center_id,
                Ticket.approved_at.isnot(None),
            )
            .order_by(Ticket.approved_at.desc(), Ticket.id.desc())
            .limit(2)
            .all()
        )
        ticket_order_date = date_to_str(
            approved_tickets[0].order_date
            or approved_tickets[0].approved_at
            or approved_tickets[0].created_at
        ) if approved_tickets else None
        previous_ticket_date = date_to_str(
            approved_tickets[1].order_date
            or approved_tickets[1].approved_at
            or approved_tickets[1].created_at
        ) if len(approved_tickets) > 1 else None
        for row in rows:
            items.append(
                TicketVisitSummaryItem(
                    product_id=row.product_id,
                    loss_last=row.loss_last,
                    loss_prev=row.loss_prev,
                    sales_last=row.sales_last,
                    sales_prev=row.sales_prev,
                    stock_last=row.stock_last,
                    stock_prev=row.stock_prev,
                    next_qty=row.next_qty,
                    order_last=row.order_last,
                    order_prev=row.order_prev,
                    order_last_date=ticket_order_date,
                    order_prev_date=previous_ticket_date,
                )
            )

        return TicketVisitSummaryResponse(ticket_id=ticket_id, items=items)
    
    @staticmethod
    def get_open_reservations(
        db: Session,
        product_ids: Optional[List[int]] = None,
    ) -> ReservationsResponse:
        statuses = ["open", "pending"]

        base_query = (
            db.query(
                TicketProduct.product_id.label("product_id"),
                TicketProduct.ticket_id.label("ticket_id"),
                Ticket.cost_center_id.label("cost_center_id"),
                TicketProduct.quantity_ordered.label("quantity"),
            )
            .join(Ticket, TicketProduct.ticket_id == Ticket.id)
            .filter(Ticket.status.in_(statuses))
        )

        if product_ids:
            normalized_ids = sorted({int(pid) for pid in product_ids})
            if normalized_ids:
                base_query = base_query.filter(TicketProduct.product_id.in_(normalized_ids))

        detail_rows = base_query.all()

        if not detail_rows:
            return ReservationsResponse(generated_at=datetime.utcnow(), items=[])

        agg: dict[int, dict] = {}
        for row in detail_rows:
            pid = row.product_id
            qty = int(row.quantity or 0)
            entry = agg.setdefault(pid, {"reserved_qty": 0, "tickets": []})
            entry["reserved_qty"] += qty
            entry["tickets"].append(
                ReservationTicketItem(
                    ticket_id=row.ticket_id,
                    cost_center_id=row.cost_center_id,
                    quantity=qty,
                )
            )

        items = [
            ReservationItem(
                product_id=pid,
                reserved_qty=data["reserved_qty"],
                tickets=data["tickets"],
            )
            for pid, data in sorted(agg.items())
        ]

        return ReservationsResponse(
            generated_at=datetime.utcnow(),
            items=items,
        )
