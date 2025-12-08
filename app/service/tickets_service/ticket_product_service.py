

from sqlalchemy.orm import Session
from app.repository.tickets.ticket_product_repository import add_product_to_ticket, get_products_ticket_by_id, get_ticket_products, remove_product_from_ticket, update_ticket_product, update_ticket_product_unit_price


class TicketProductService:
    
    @staticmethod
    def add_product( product_data,db):
        return add_product_to_ticket(db, product_data)


 
    @staticmethod
    def get_products_for_ticket(db, ticket_id):
        return get_products_ticket_by_id(db, ticket_id)
    
  

    @staticmethod
    def remove_product(db, ticket_product_id):
        return remove_product_from_ticket(db, ticket_product_id)
    @staticmethod
    def set_ticket_product_unit_price(db: Session, ticket_product_id: int, unit_price: float):
        if unit_price is None or unit_price < 0:
            raise ValueError("unit_price inválido")
        tp = update_ticket_product_unit_price(db, ticket_product_id, unit_price)
        return tp
    
    @staticmethod
    def update_ticket_product_service(db: Session, ticket_id: int, product_id: int, updates: dict):
        return update_ticket_product(db, ticket_id, product_id, updates)
