from datetime import datetime
from fastapi import HTTPException
from pytest import Session
from app.models.stockMovement import MovementType, StockMovement
from app.repository.stock.stock_movement_repository import create_stock_movements_for_sales, move_stock_to_cost_center
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
    
    
    @staticmethod
    def process_sales(ticket: TicketRegisterSales, db: Session):
        try:
            create_stock_movements_for_sales(ticket.products, ticket.cost_center_id, db)

            # Atualiza os produtos do ticket (substitui os antigos pelos novos)
            updated_ticket = TicketService.update_ticket_products_with_sales(ticket, db)


            return updated_ticket
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Erro ao processar venda: {str(e)}")

    @staticmethod
    def update_ticket_products_with_sales(ticket, db: Session):
        existing_products = {
            tp.product_id: tp for tp in db.query(TicketProduct).filter(TicketProduct.ticket_id == ticket.id).all()
        }

        updated_ticket_products = []

        for tp in ticket.products:
            data = tp.dict(exclude={'ticket_id'})
            product_id = data['product_id']
            new_qtd_sold = data.get('quantity_sold', 0)

            if product_id in existing_products:
                old_tp = existing_products[product_id]
                delta = new_qtd_sold - old_tp.quantity_sold
                if delta > 0:
                    db.add(StockMovement(
                        product_id=product_id,
                        quantity=delta,
                        movement_type=MovementType.SOLD,
                        cost_center_id=ticket.cost_center_id,
                        supplier=None
                    ))
                # Atualiza os dados existentes
                for key, value in data.items():
                    setattr(old_tp, key, value)
                updated_ticket_products.append(old_tp)

            else:
                # Novo produto vinculado ao ticket
                new_tp = TicketProduct(**data, ticket_id=ticket.id)
                db.add(new_tp)
                updated_ticket_products.append(new_tp)

                if new_qtd_sold > 0:
                    db.add(StockMovement(
                        product_id=product_id,
                        quantity=new_qtd_sold,
                        movement_type=MovementType.OUT,
                        cost_center_id=data['cost_center_id'],
                        supplier=None
                    ))

        db.commit()

        # Retorna o ticket atualizado, incluindo os produtos
        updated_ticket = db.query(Ticket).filter(Ticket.id == ticket.id).options(
            joinedload(Ticket.products)
        ).first()

        return updated_ticket



