
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.tickets import Ticket, TicketProduct


def add_product_to_ticket(db, product_data):
    product = (
        db.query(Product)
        .filter(
            Product.id == product_data.product_id,
            Product.is_active == True,
            Product.deleted_at.is_(None),
        )
        .first()
    )
    ticket_product = TicketProduct(
    **product_data.dict(),
)
    db.add(ticket_product)
    db.commit()
    db.refresh(ticket_product)
    return ticket_product

def remove_product_from_ticket(db, ticket_product_id):
    ticket_product = db.query(TicketProduct).filter(TicketProduct.id == ticket_product_id).first()
    if ticket_product:
        db.delete(ticket_product)
        db.commit()
    return ticket_product

def update_ticket_product_unit_price(db: Session, ticket_product_id: int, unit_price: float) -> TicketProduct | None:
    tp = db.query(TicketProduct).filter(TicketProduct.id == ticket_product_id).first()
    if not tp:
        return None
    tp.unit_price = unit_price
    db.commit()
    db.refresh(tp)
    return tp

def update_ticket_product(db: Session, ticket_id: int, product_id: int, updates: dict):
    tp = (
        db.query(TicketProduct)
        .filter(TicketProduct.ticket_id == ticket_id, TicketProduct.product_id == product_id)
        .first()
    )
    
    for key, value in updates.items():
        if hasattr(tp, key):
            setattr(tp, key, value)

    db.commit()
    db.refresh(tp)
    return tp


def get_products_by_ticket(db, ticket_id):
    return db.query(TicketProduct).filter(TicketProduct.ticket_id == ticket_id).order_by(TicketProduct.id).all()


def get_products_ticket_by_id(db, ticket_id):
    return [product.product_id for product in db.query(TicketProduct).filter(TicketProduct.ticket_id == ticket_id).order_by(TicketProduct.id).all()]

def get_ticket_products(db):
    return db.query(TicketProduct).order_by(TicketProduct.id).all()



def get_ticket_products_by_cost_center(db: Session, cost_center_id: int):
    return (
        db.query(TicketProduct)
        .join(Ticket)
        .filter(Ticket.cost_center_id == cost_center_id)
        .all()
    )
    
