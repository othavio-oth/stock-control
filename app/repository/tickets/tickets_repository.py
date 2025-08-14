from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from app.models.stockMovement import StockMovement
from app.schemas.stock_schemas.stock_movement_schema import StockMovementRead, StockMovementSaleCreate
from app.schemas.tickets_schemas.tickets_schemas import TicketProductBase
from . import *
from sqlalchemy.orm import joinedload
from sqlalchemy import desc, or_

def search_tickets_any( search_term: str,page:int,db: Session):
    page_size = 20
    offset = (page - 1) * page_size
    base_query = (
        db.query(Ticket)
          .options(joinedload(Ticket.products).joinedload(TicketProduct.product))  # <-- aqui
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
    "total": total,
    "page": page,
    "page_size": page_size,
    "total_pages": total_pages
    }


def get_all_tickets(page:int,db: Session):
    page_size = 20
    offset = (page - 1) * page_size
    total = db.query(Ticket).count()
    tickets = db.query(Ticket).options(joinedload(Ticket.products).joinedload(TicketProduct.product)).offset(offset).limit(page_size).all()
    total_pages = (total + page_size - 1) // page_size
    return {
    "items": tickets,
    "total": total,
    "page": page,
    "page_size": page_size,
    "total_pages": total_pages
    }

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).options(joinedload(Ticket.products)).filter(Ticket.id == ticket_id).first()

# tickets_repository.py
from sqlalchemy.orm import Session, joinedload
from app.models.tickets import Ticket, TicketProduct

def _to_dict(obj, **kwargs):
    # v2
    if hasattr(obj, "model_dump"):
        return obj.model_dump(**kwargs)
    # v1
    if hasattr(obj, "dict"):
        return obj.dict(**kwargs)
    # já é dict
    return obj

def create_ticket(db: Session, ticket_data):
    # 1) se vierem produtos no payload
    items = getattr(ticket_data, "products", []) or []

    # 2) remover "products" antes de instanciar Ticket
    data = _to_dict(ticket_data, exclude={"products"})
    ticket = Ticket(**data)  # <-- sem .dict()
    db.add(ticket)
    db.flush()  # garante ticket.id

    # 3) criar TicketProduct para cada item
    for it in items:
        itd = _to_dict(it)
        tp = TicketProduct(
            ticket_id=ticket.id,
            product_id=itd["product_id"],
            quantity_ordered=itd["quantity_ordered"],  # alias 'quantity' já resolvido no schema
            unit_price=itd.get("unit_price"),
            entry_price=itd.get("entry_price"),
        )
        db.add(tp)

    db.commit()

    # 4) retornar já com relacionamentos carregados
    ticket = (
        db.query(Ticket)
          .options(joinedload(Ticket.products).joinedload(TicketProduct.product))
          .get(ticket.id)
    )
    return ticket



def update_ticket(db, ticket_id, ticket_data):
    ticket = get_ticket_by_id(db, ticket_id)
    if ticket:
        for key, value in ticket_data.dict().items():
            setattr(ticket, key, value)
        db.commit()
        db.refresh(ticket)
    return ticket

def delete_ticket(db, ticket_id):
    ticket = get_ticket_by_id(db, ticket_id)
    if ticket:
        db.delete(ticket)
        db.commit()
    return None

def get_products_by_ticket(db, ticket_id):
    return db.query(TicketProduct).filter(TicketProduct.ticket_id == ticket_id).order_by(TicketProduct.id).all()

def add_product_to_ticket(db, product_data):
    product = db.query(Product).filter(Product.id == product_data.product_id).first()
    ticket_product = TicketProduct(
    **product_data.dict(),
)
    db.add(ticket_product)
    db.commit()
    db.refresh(ticket_product)
    return ticket_product

def get_products_ticket_by_id(db, ticket_id):
    return [product.product_id for product in db.query(TicketProduct).filter(TicketProduct.ticket_id == ticket_id).order_by(TicketProduct.id).all()]

def get_ticket_products(db):
    return db.query(TicketProduct).order_by(TicketProduct.id).all()

def remove_product_from_ticket(db, ticket_product_id):
    ticket_product = db.query(TicketProduct).filter(TicketProduct.id == ticket_product_id).first()
    if ticket_product:
        db.delete(ticket_product)
        db.commit()
    return ticket_product

def get_ticket_products_by_cost_center(db: Session, cost_center_id: int):
    return (
        db.query(TicketProduct)
        .join(Ticket)
        .filter(Ticket.cost_center_id == cost_center_id)
        .all()
    )
    
def update_ticket_product_unit_price(db: Session, ticket_product_id: int, unit_price: float) -> TicketProduct | None:
    tp = db.query(TicketProduct).filter(TicketProduct.id == ticket_product_id).first()
    if not tp:
        return None
    tp.unit_price = unit_price
    db.commit()
    db.refresh(tp)
    return tp

def get_last_approved_ticket_id_for_cc_product(
    db: Session, cost_center_id: int, product_id: int
) -> Optional[int]:
    """
    Retorna o ID do último ticket aprovado para (cost_center_id, product_id).
    Preferência: approved_at mais recente. Fallback: status == 'APPROVED'.
    """
    # 1) Preferência: approved_at definido
    q1 = (
        db.query(Ticket.id)
        .join(TicketProduct, TicketProduct.ticket_id == Ticket.id)
        .filter(
            Ticket.cost_center_id == cost_center_id,
            TicketProduct.product_id == product_id,
            Ticket.approved_at.isnot(None),         # requer o campo approved_at
        )
        .order_by(desc(Ticket.approved_at), desc(Ticket.id))
        .limit(1)
    ).first()
    if q1:
        return q1[0]