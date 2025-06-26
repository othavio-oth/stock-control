from app.repository.tickets.tickets_repository import create_ticket, get_all_tickets, get_ticket_by_id, update_ticket, delete_ticket, add_product_to_ticket, get_products_by_ticket, get_products_ticket_by_id, get_ticket_products, remove_product_from_ticket
from app.models.tickets import Ticket, TicketProduct

class TicketService:
    @staticmethod
    def list_tickets(db):
        return get_all_tickets(db)

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
            raise ValueError("Ticket não encontrada.")
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