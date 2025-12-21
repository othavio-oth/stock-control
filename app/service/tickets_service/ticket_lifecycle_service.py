from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.stockMovement import MovementType, StockMovement
from app.models.tickets import Ticket, TicketProduct
from app.repository.stock.stock_movement_repository import process_stock_movement
from app.repository.tickets.tickets_repository import get_last_approved_ticket_id_for_cc_product, get_previous_approved_ticket_for_cost_center, get_ticket_by_id
from sqlalchemy.orm import joinedload

from starlette.status import HTTP_404_NOT_FOUND


class TicketLifecycleService:

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

        # 2) Cria as movimentações TO_CLIENT (saída do inventário / entrada no cliente)
        for tp in ticket.products:
            product = (
                db.query(Product)
                .filter(
                    Product.id == tp.product_id,
                    Product.is_active == True,
                    Product.deleted_at.is_(None),
                )
                .first()
            )
            if not product:
                raise HTTPException(status_code=404, detail=f"Produto {tp.product_id} não encontrado")

            movement = StockMovement(
                product_id=tp.product_id,
                quantity=tp.sent_quantity,
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
    def get_previous_approved_ticket_service(db: Session, ticket_id: int) -> Ticket:
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Ticket nǜo encontrado.")

        previous = get_previous_approved_ticket_for_cost_center(
            db,
            cost_center_id=ticket.cost_center_id,
            current_ticket_id=ticket.id,
        )
        if not previous:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Nenhum ticket aprovado anterior encontrado para este cost center.",
            )
        return previous

    
