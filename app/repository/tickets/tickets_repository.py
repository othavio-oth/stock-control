from . import *
from sqlalchemy.orm import joinedload

def get_all_tickets(db: Session):
    tickets = db.query(Ticket).options(joinedload(Ticket.products).joinedload(TicketProduct.product)).all()
    return tickets

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