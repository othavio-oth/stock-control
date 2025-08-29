from datetime import datetime, timedelta
from typing import Optional
import re
from fastapi import HTTPException
from pytest import Session
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.models.product import Product
from app.models.stockMovement import InventoryStock, MovementType, StockMovement
from app.repository.stock.stock_movement_repository import process_stock_movement
from app.repository.tickets.tickets_repository import create_ticket, get_all_tickets, get_last_approved_ticket_id_for_cc_product, get_ticket_by_id, search_tickets_any, update_ticket, delete_ticket, add_product_to_ticket, get_products_by_ticket, get_products_ticket_by_id, get_ticket_products, remove_product_from_ticket, update_ticket_product, update_ticket_product_unit_price
from app.models.tickets import Ticket, TicketProduct
from app.schemas.stock_schemas.stock_movement_schema import  StockMovementSaleCreate
from app.schemas.tickets_schemas.tickets_schemas import TicketRegisterSales
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from sqlalchemy.exc import IntegrityError




class TicketService:
    @staticmethod
    def list_tickets(page,db):
        return get_all_tickets(page,db)

    @staticmethod
    def create_ticket(db, ticket_data):
        base_name = ticket_data.name
        existing_tickets = (
            db.query(Ticket)
            .filter(Ticket.name.like(f"{base_name}%"))
            .all()
        )

        if existing_tickets:
            # Extrai números existentes no formato "- #n"
            max_num = 0
            for t in existing_tickets:
                if " - #" in t.name:
                    try:
                        num = int(t.name.split(" - #")[-1])
                        max_num = max(max_num, num)
                    except ValueError:
                        pass
                else:
                    # Esse é o original sem sufixo
                    max_num = max(max_num, 0)

            ticket_data.name = f"{base_name} - #{max_num + 1}"

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

   
    @staticmethod
    def set_ticket_product_unit_price(db: Session, ticket_product_id: int, unit_price: float):
        if unit_price is None or unit_price < 0:
            raise ValueError("unit_price inválido")
        tp = update_ticket_product_unit_price(db, ticket_product_id, unit_price)
        return tp
    
    
    @staticmethod
    def approve_ticket(ticket_id: int, db: Session):
        # 1) Carrega o ticket com os produtos
        ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket não encontrado")

        if (ticket.status or "").lower() == "approved":
            raise HTTPException(status_code=400, detail="Ticket já aprovado")

        if not ticket.products or len(ticket.products) == 0:
            raise HTTPException(status_code=400, detail="Ticket sem produtos")

        # 2) Valida estoque do inventário antes de movimentar
        insuficientes = []
        for tp in ticket.products:
            inv = db.query(InventoryStock).filter(InventoryStock.product_id == tp.product_id).first()
            if not inv or inv.quantity < tp.quantity_ordered:
                insuficientes.append({"product_id": tp.product_id, "requisitado": tp.quantity_ordered, "disponivel": inv.quantity if inv else 0})

        if insuficientes:
            raise HTTPException(
                status_code=400,
                detail={"erro": "Estoque insuficiente no inventário para alguns itens", "itens": insuficientes}
            )

        # 3) Cria as movimentações TO_CLIENT (saída do inventário / entrada no cliente)
        for tp in ticket.products:
            product = db.query(Product).filter(Product.id == tp.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Produto {tp.product_id} não encontrado")

            movement = StockMovement(
                product_id=tp.product_id,
                quantity=tp.quantity_ordered,
                movement_type=MovementType.TO_CLIENT,      
                cost_center_id=ticket.cost_center_id,
                product_unit_cost=(product.current_cost if product.current_cost is not None else None),
                created_at=datetime.now(),
            )
            db.add(movement)
            process_stock_movement(db, movement)
            db.flush()  # garante ID se necessário

            # Atualiza estoques (InventoryStock ↓ / ClientStock ↑)

        # 4) Marca ticket como aprovado e confirma
        ticket.status = "approved"
        ticket.approved_at = datetime.now()
        ticket.sales_start_date = ticket.approved_at + timedelta(days=1)
        db.commit()
        db.refresh(ticket)

        return ticket
    
    @staticmethod
    def get_last_approved_ticket_id_service(db: Session, cost_center_id: int, product_id: Optional[int]
    ) -> dict:
        ticket_id = get_last_approved_ticket_id_for_cc_product(db, cost_center_id, product_id)
        if not ticket_id:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Nenhum ticket aprovado encontrado para este produto/centro de custo.",
            )
        # Carrega o ticket completo com produtos (e dados do produto)
        ticket = (
            db.query(Ticket)
            .options(joinedload(Ticket.products).joinedload(TicketProduct.product))
            .filter(Ticket.id == ticket_id)
            .first()
        )
        if not ticket:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Ticket não encontrado após localizar o ID aprovado.",
            )
        return ticket
    

    @staticmethod
    def update_ticket_product_service(db: Session, ticket_id: int, product_id: int, updates: dict):
        return update_ticket_product(db, ticket_id, product_id, updates)
