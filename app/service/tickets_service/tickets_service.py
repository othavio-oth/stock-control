from datetime import datetime
from fastapi import HTTPException
from pytest import Session
from app.repository.tickets.tickets_repository import create_ticket, get_all_tickets, get_ticket_by_id, search_tickets_any, update_ticket, delete_ticket, add_product_to_ticket, get_products_by_ticket, get_products_ticket_by_id, get_ticket_products, remove_product_from_ticket
from app.models.tickets import Ticket, TicketProduct
from app.schemas.stock_schemas.stock_movement_schema import  StockMovementSaleCreate
from app.schemas.tickets_schemas.tickets_schemas import TicketRegisterSales
from sqlalchemy.orm import joinedload


class TicketService:
    @staticmethod
    def list_tickets(page,db):
        return get_all_tickets(page,db)

    @staticmethod
    def create_ticket(db, ticket_data):
        existing_ticket = db.query(Ticket).filter(Ticket.name == ticket_data.name).first()
        if existing_ticket:
            raise ValueError("Ticket com este nome já existe.")
        return create_ticket(db, ticket_data)

    @staticmethod
    def edit_ticket(db, ticket_id, ticket_data):
        if not get_ticket_by_id(db, ticket_id):
            raise ValueError("Ticket não encontrada.")
        return update_ticket(db, ticket_id, ticket_data)

    @staticmethod
    def remove_ticket(db, ticket_id):
        if not get_ticket_by_id(db, ticket_id):
            raise ValueError("Ticket não encontrado.")
        return delete_ticket(db, ticket_id)

    @staticmethod
    def add_product(db, product_data):
        return add_product_to_ticket(db, product_data)

    @staticmethod
    def get_products_for_ticket(db, ticket_id):
        return get_products_ticket_by_id(db, ticket_id)
    
    def service_get_ticket_products(db):
        return get_ticket_products(db)

    @staticmethod
    def remove_product(db, ticket_product_id):
        return remove_product_from_ticket(db, ticket_product_id)
    
    @staticmethod
    def search_tickets_by_term( search_term,page, db):
        return search_tickets_any( search_term,page, db)
    
    @staticmethod
    def close_ticket_and_move_stock(ticket_id, db):
       
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
     

        return ticket
    
    
    @staticmethod
    def process_sales(ticket: TicketRegisterSales, db: Session):
        try:

            updated_ticket = TicketService.update_ticket_products_with_sales(ticket, db)


            return updated_ticket
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao processar venda: {str(e)}")

   


