from fastapi import HTTPException
from app.models.stockMovement import MovementType
from app.repository.stock.stock_movement_repository import move_stock_to_cost_center
from app.repository.tickets.tickets_repository import create_ticket, get_all_tickets, get_ticket_by_id, search_tickets_any, update_ticket, delete_ticket, add_product_to_ticket, get_products_by_ticket, get_products_ticket_by_id, get_ticket_products, remove_product_from_ticket
from app.models.tickets import Ticket, TicketProduct
from app.schemas.stock_schemas.stock_movement_schema import StockMovementSaleCreate

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
    
    @staticmethod
    def search_tickets_by_term( search_term,page, db):
        return search_tickets_any( search_term,page, db)
    
    @staticmethod
    def close_ticket_and_move_stock(ticket_id, db):
       
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        if ticket.status == "closed":
            raise HTTPException(status_code=400, detail="Ticket already closed")

        
        if ticket.cost_center_id is None:
            raise HTTPException(status_code=400, detail="Ticket must have a cost center")

        
        ticket_products = db.query(TicketProduct).filter(TicketProduct.ticket_id == ticket_id).all()

        # 4. Para cada produto, cria um StockMovement
        for tp in ticket_products:
            movement_data = StockMovementSaleCreate(
                product_id=tp.product_id,
                quantity=tp.quantity_ordered,
                movement_type=MovementType.TO_COST_CENTER,
                cost_center_id=ticket.cost_center_id
            )
            
            move_stock_to_cost_center(movement_data, db)

        # 5. Atualiza o status do ticket
        ticket.status = "closed"
        db.commit()
        db.refresh(ticket)

        return ticket

