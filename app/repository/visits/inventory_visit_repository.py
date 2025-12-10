from datetime import date, datetime
from typing import Iterable, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.stockMovement import InventoryVisit, InventoryVisitProduct
from sqlalchemy.orm import joinedload

from app.models.tickets import Ticket
from app.repository.stock.client_stock_repository import (
    get_client_stock_by_cost_center,
    sync_client_stock_from_snapshot,
    zero_absent_client_stock_entries,
)
from app.repository.tickets.ticket_queries import recalculate_daily_visit_history


def create_inventory_visit_record(
    db: Session,
    *,
    ticket: Ticket,
    recorded_by: Optional[int],
    visited_at: datetime,
    total_stock_quantity: Optional[int],
    notes: Optional[str],
    product_entries: Iterable[dict],
) -> InventoryVisit:
    entries = list(product_entries)
    visit = InventoryVisit(
        cost_center_id=ticket.cost_center_id,
        ticket_id=ticket.id,
        recorded_by=recorded_by,
        visited_at=visited_at,
        total_stock_quantity=total_stock_quantity,
        notes=notes,
    )
    db.add(visit)
    db.flush()

    total_from_products = 0
    product_ids: set[int] = set()
    for entry in entries:
        try:
            product_id = int(entry["product_id"])
        except (KeyError, TypeError, ValueError):
            raise ValueError("product_entries deve conter product_id válido")
        product_ids.add(product_id)

    previous_stock_rows = get_client_stock_by_cost_center(
        db,
        cost_center_id=ticket.cost_center_id,
        product_ids=product_ids,
        include_zero=True,
    )
    previous_stock_map = {
        row["product_id"]: int(row.get("quantity", 0) or 0) for row in previous_stock_rows
    }

    for entry in entries:
        stock_qty = int(entry.get("stock_quantity", 0))
        try:
            product_id = int(entry["product_id"])
        except (KeyError, TypeError, ValueError):
            raise ValueError("product_entries deve conter product_id válido")
        next_qty = entry.get("next_qty", entry.get("nextQty"))
        next_qty_int = int(next_qty) if next_qty is not None else None
        shelf_price = entry.get("shelf_price", entry.get("shelfPrice"))
        product_visit = InventoryVisitProduct(
            inventory_visit_id=visit.id,
            product_id=product_id,
            stock_quantity=stock_qty,
            previous_client_stock=previous_stock_map.get(product_id),
            sales_quantity=int(entry.get("sales_quantity", 0) or 0),
            loss_quantity=int(entry.get("loss_quantity", 0) or 0),
            next_quantity=next_qty_int,
            shelf_price=shelf_price,
        )
        total_from_products += stock_qty
        db.add(product_visit)

    if total_stock_quantity is None:
        visit.total_stock_quantity = total_from_products

    sync_client_stock_from_snapshot(
        db,
        cost_center_id=ticket.cost_center_id,
        product_quantities=entries,
        observed_at=visit.visited_at,
    )
    db.flush()

    zero_absent_client_stock_entries(
        db,
        cost_center_id=ticket.cost_center_id,
        observed_product_ids=product_ids,
        zeroed_at=visit.visited_at,
    )

    visit_date = visit.visited_at.date()
    recalculate_daily_visit_history(
        db,
        cost_center_id=ticket.cost_center_id,
        date_product_map={visit_date: product_ids},
    )

    db.commit()
    db.refresh(visit)
    return visit


def update_inventory_visit_record(
    db: Session,
    *,
    ticket: Ticket,
    visit_id: int,
    recorded_by: Optional[int],
    visited_at: Optional[datetime],
    total_stock_quantity: Optional[int],
    notes: Optional[str],
    product_entries: Optional[Iterable[dict]],
    editor_user_id: Optional[int],
    allow_admin: bool,
) -> InventoryVisit:
    visit = (
        db.query(InventoryVisit)
        .options(joinedload(InventoryVisit.products))
        .filter(InventoryVisit.id == visit_id, InventoryVisit.ticket_id == ticket.id)
        .first()
    )
    if not visit:
        raise HTTPException(status_code=404, detail="Visita não encontrada para este ticket.")

    if not allow_admin:
        if not editor_user_id or visit.recorded_by != editor_user_id:
            raise HTTPException(
                status_code=403,
                detail="Você só pode visualizar ou editar visitas registradas por você.",
            )

    previous_visit_date = visit.visited_at.date()
    previous_product_ids = {p.product_id for p in visit.products}
    existing_previous_stock = {p.product_id: p.previous_client_stock for p in visit.products}

    if visited_at is not None:
        visit.visited_at = visited_at
    if notes is not None:
        visit.notes = notes
    if recorded_by is not None:
        visit.recorded_by = recorded_by

    recalculated_total: Optional[int] = None
    new_product_ids: set[int] = set()
    if product_entries is not None:
        entries = list(product_entries)
        visit.products.clear()
        db.flush()
        total_from_products = 0
        for entry in entries:
            stock_qty = int(entry.get("stock_quantity", 0) or 0)
            try:
                product_id = int(entry["product_id"])
            except (KeyError, TypeError, ValueError):
                raise ValueError("product_entries deve conter product_id válido")
            previous_stock = existing_previous_stock.get(product_id)
            if previous_stock is None:
                raw_previous = entry.get("previous_client_stock", entry.get("previousClientStock"))
                if raw_previous is not None:
                    try:
                        previous_stock = int(raw_previous)
                    except (TypeError, ValueError):
                        previous_stock = None
            next_qty = entry.get("next_qty", entry.get("nextQty"))
            next_qty_int = int(next_qty) if next_qty is not None else None
            shelf_price = entry.get("shelf_price", entry.get("shelfPrice"))
            product_visit = InventoryVisitProduct(
                inventory_visit_id=visit.id,
                product_id=product_id,
                stock_quantity=stock_qty,
                previous_client_stock=previous_stock,
                sales_quantity=int(entry.get("sales_quantity", 0) or 0),
                loss_quantity=int(entry.get("loss_quantity", 0) or 0),
                next_quantity=next_qty_int,
                shelf_price=shelf_price,
            )
            total_from_products += stock_qty
            visit.products.append(product_visit)
            new_product_ids.add(product_id)
        recalculated_total = total_from_products

        sync_client_stock_from_snapshot(
            db,
            cost_center_id=ticket.cost_center_id,
            product_quantities=entries,
            observed_at=visit.visited_at,
        )
        db.flush()
    else:
        new_product_ids = {p.product_id for p in visit.products}

    zero_absent_client_stock_entries(
        db,
        cost_center_id=ticket.cost_center_id,
        observed_product_ids=new_product_ids,
        zeroed_at=visit.visited_at,
    )

    if total_stock_quantity is not None:
        visit.total_stock_quantity = total_stock_quantity
    elif recalculated_total is not None:
        visit.total_stock_quantity = recalculated_total

    current_visit_date = visit.visited_at.date()
    date_product_map: dict[date, set[int]] = {}
    if previous_product_ids:
        date_product_map.setdefault(previous_visit_date, set()).update(previous_product_ids)
    if new_product_ids:
        date_product_map.setdefault(current_visit_date, set()).update(new_product_ids)
    elif current_visit_date not in date_product_map:
        date_product_map[current_visit_date] = set()

    recalculate_daily_visit_history(
        db,
        cost_center_id=ticket.cost_center_id,
        date_product_map=date_product_map,
    )

    db.commit()
    db.refresh(visit)
    return visit


def list_inventory_visits_by_ticket(db: Session, ticket_id: int) -> list[InventoryVisit]:
    return (
        db.query(InventoryVisit)
        .options(
            joinedload(InventoryVisit.products).joinedload(InventoryVisitProduct.product),
            joinedload(InventoryVisit.cost_center),
        )
        .filter(InventoryVisit.ticket_id == ticket_id)
        .order_by(InventoryVisit.visited_at.desc())
        .all()
    )


def list_all_inventory_visits_paginated(
    
    
    db: Session,
    *,
    page: int,
    page_size: int,
) -> dict:
    offset = (page - 1) * page_size

    query = (
        db.query(InventoryVisit)
        .options(
            joinedload(InventoryVisit.products).joinedload(InventoryVisitProduct.product),
            joinedload(InventoryVisit.cost_center),
        )
        .order_by(InventoryVisit.visited_at.desc(), InventoryVisit.id.desc())
    )

    total = query.count()
    visits = query.offset(offset).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size if page_size else 0

    return {
        "items": visits,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }
    
def get_previous_inventory_snapshot(
    db: Session,
    *,
    cost_center_id: int,
    product_id: int,
    before_visit_id: int,
    before_visited_at: Optional[datetime],
):
    query = (
        db.query(
            InventoryVisitProduct.stock_quantity.label("previous_quantity"),
            InventoryVisit.visited_at.label("previous_visited_at"),
        )
        .join(InventoryVisit, InventoryVisit.id == InventoryVisitProduct.inventory_visit_id)
        .filter(
            InventoryVisit.cost_center_id == cost_center_id,
            InventoryVisitProduct.product_id == product_id,
        )
    )

    if before_visited_at:
        query = query.filter(
            or_(
                InventoryVisit.visited_at < before_visited_at,
                and_(
                    InventoryVisit.visited_at == before_visited_at,
                    InventoryVisit.id < before_visit_id,
                ),
            )
        )
    else:
        query = query.filter(InventoryVisit.id < before_visit_id)

    return (
        query.order_by(InventoryVisit.visited_at.desc(), InventoryVisit.id.desc())
        .limit(1)
        .first()
    )
