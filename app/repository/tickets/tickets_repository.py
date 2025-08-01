from datetime import datetime

from fastapi import HTTPException
from app.models.stockMovement import StockMovement
from app.schemas.stock_schemas.stock_movement_schema import StockMovementRead, StockMovementSaleCreate
from app.schemas.tickets_schemas.tickets_schemas import TicketProductBase
from . import *
from sqlalchemy.orm import joinedload
from sqlalchemy import or_

def search_tickets_any( search_term: str,page:int,db: Session):
    page_size = 20
    offset = (page - 1) * page_size
    base_query = db.query(Ticket).join(CostCenter).filter(
            or_(
                Ticket.id == int(search_term) if search_term.isdigit() else False,
                Ticket.name.ilike(f"%{search_term}%"),
                CostCenter.name.ilike(f"%{search_term}%")
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

def create_ticket(db, ticket_data):
    ticket = Ticket(**ticket_data.dict())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
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
    return ticket

def get_products_by_ticket(db, ticket_id):
    return db.query(TicketProduct).filter(TicketProduct.ticket_id == ticket_id).order_by(TicketProduct.id).all()

def add_product_to_ticket(db, product_data):
    ticket_product = TicketProduct(**product_data.dict())
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
    

    


