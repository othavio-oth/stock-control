from datetime import datetime, timedelta, date, timezone
from typing import Optional, List
import re
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, or_, text
from sqlalchemy.orm import joinedload
from app.models.product import Product
from app.models.stockMovement import (
    InventoryVisit,

)
from app.repository.stock.stock_movement_repository import process_stock_movement
from app.repository.stock.client_stock_repository import get_client_stock_by_cost_center
from app.repository.tickets.ticket_product_repository import update_ticket_product_unit_price
from app.repository.tickets.ticket_queries import search_tickets_any
from app.repository.tickets.tickets_repository import (
    create_ticket,
    get_all_tickets,
    get_ticket_by_id,

    update_ticket,
    delete_ticket,
    get_products_by_ticket,

    get_previous_approved_ticket_for_cost_center,
)
from app.repository.visits.inventory_visit_repository import create_inventory_visit_record, get_previous_inventory_snapshot, list_all_inventory_visits_paginated, list_inventory_visits_by_ticket, update_inventory_visit_record
from app.service.utils.date_utils import date_to_str
from app.service.users_service.permission_service import PermissionService
from app.models.tickets import Ticket, TicketProduct
from app.schemas.tickets_schemas.tickets_schemas import TicketRegisterSales
from app.schemas.tickets_schemas.inventory_visit_schema import (
    InventoryVisitCreate,
    InventoryVisitUpdate,
    InventoryVisitHistoryPaginatedResponse,
    InventoryVisitProductWithHistoryResponse,
    InventoryVisitWithHistoryResponse,
    TicketCycleProductsResponse,
    ProductCycleTimelineResponse,
    ProductCycleBlock,
    ProductVisitSnapshot,
    CostCenterProductVisitsResponse,
    CostCenterLatestVisitsResponse,
    CostCenterVisitSnapshot,
    VisitProductSnapshot,
    TicketVisitSummaryResponse,
    TicketVisitSummaryItem,
    LastVisitNextQtyResponse,
    LastVisitProductNextQty,
    ReservationsResponse,
    ReservationItem,
    ReservationTicketItem,
)
from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from sqlalchemy.exc import IntegrityError

from app.service.utils.ticket_utils import get_allowed_ticket_ids
from app.service.utils.visit_utils import build_cycle_block, collect_visits_by_product

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
        current = get_ticket_by_id(db, ticket_id)
        if not current:
            raise ValueError("Ticket não encontrada.")
        # Garantir unicidade do nome ao editar
        try:
            new_name = getattr(ticket_data, "name", None)
        except Exception:
            new_name = None
        if new_name:
           
            others = (
                db.query(Ticket)
                .filter(Ticket.id != ticket_id, Ticket.name.like(f"{new_name}%"))
                .all()
            )
            if others:
                max_num = 0
                exact_collision = False
                for t in others:
                    if t.name == new_name:
                        exact_collision = True
                    if " - #" in t.name:
                        try:
                            num = int(t.name.split(" - #")[-1])
                            max_num = max(max_num, num)
                        except ValueError:
                            pass
                if exact_collision:
                    # Aplica sufixo incremental como no create
                    ticket_data.name = f"{new_name} - #{max_num + 1}"
        return update_ticket(db, ticket_id, ticket_data)

    @staticmethod
    def remove_ticket(db, ticket_id):
        if not get_ticket_by_id(db, ticket_id):
            raise ValueError("Ticket não encontrado.")
        return delete_ticket(db, ticket_id)


    
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
    def register_inventory_visit(
        db: Session,
        ticket_id: int,
        visit_data: InventoryVisitCreate,
        recorded_by: Optional[int],
    ):
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket nǜo encontrado")

        if not visit_data.products:
            raise HTTPException(status_code=400, detail="products nǜo pode ser vazio")

        visited_at = visit_data.visited_at or datetime.now()
        product_entries = [p.model_dump() for p in visit_data.products]
        return create_inventory_visit_record(
            db,
            ticket=ticket,
            recorded_by=recorded_by,
            visited_at=visited_at,
            total_stock_quantity=visit_data.total_stock_quantity,
            notes=visit_data.notes,
            product_entries=product_entries,
        )

    @staticmethod
    def update_inventory_visit(
        db: Session,
        ticket_id: int,
        visit_id: int,
        visit_data: InventoryVisitUpdate,
        user_id: Optional[int],
    ):
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket nuo encontrado")

        product_entries = None
        if visit_data.products is not None:
            if len(visit_data.products) == 0:
                raise HTTPException(status_code=400, detail="products nǜo pode ser vazio")
            product_entries = [p.model_dump() for p in visit_data.products]

        is_admin = PermissionService.user_is_admin(db, user_id)
        return update_inventory_visit_record(
            db,
            ticket=ticket,
            visit_id=visit_id,
            recorded_by=None,
            visited_at=visit_data.visited_at,
            total_stock_quantity=visit_data.total_stock_quantity,
            notes=visit_data.notes,
            product_entries=product_entries,
            editor_user_id=user_id,
            allow_admin=is_admin,
        )

    @staticmethod
    def list_inventory_visits(db: Session, ticket_id: int, current_user_id: Optional[int]):
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket nuo encontrado")
        visits = list_inventory_visits_by_ticket(db, ticket_id)

        if PermissionService.user_is_admin(db, current_user_id):
            return visits
        return [
            visit for visit in visits
            if visit.recorded_by == current_user_id
        ]



 
    @staticmethod
    def get_cost_center_last_visit_next_qty(
        db: Session,
        cost_center_id: int,
    ) -> LastVisitNextQtyResponse:
        visit = (
            db.query(InventoryVisit)
            .options(joinedload(InventoryVisit.products))
            .filter(InventoryVisit.cost_center_id == cost_center_id)
            .order_by(InventoryVisit.visited_at.desc(), InventoryVisit.id.desc())
            .first()
        )
        if not visit:
            return LastVisitNextQtyResponse(
                cost_center_id=cost_center_id,
                visit_id=None,
                visited_at=None,
                products=[],
            )

        products = [
            LastVisitProductNextQty(
                product_id=p.product_id,
                next_qty=p.next_quantity,
            )
            for p in (visit.products or [])
        ]

        return LastVisitNextQtyResponse(
            cost_center_id=cost_center_id,
            visit_id=visit.id,
            visited_at=date_to_str(visit.visited_at),
            products=products,
        )

 


    @staticmethod
    def list_all_inventory_visits(db: Session, page: int, page_size: int):
        data = list_all_inventory_visits_paginated(db, page=page, page_size=page_size)
        visit_payloads: list[InventoryVisitWithHistoryResponse] = []

        for visit in data["items"]:
            product_payloads: list[InventoryVisitProductWithHistoryResponse] = []
            for product in visit.products:
                prev = get_previous_inventory_snapshot(
                    db,
                    cost_center_id=visit.cost_center_id,
                    product_id=product.product_id,
                    before_visit_id=visit.id,
                    before_visited_at=visit.visited_at,
                )
                product_payloads.append(
                    InventoryVisitProductWithHistoryResponse(
                        product_id=product.product_id,
                        stock_quantity=product.stock_quantity,
                        previous_client_stock=int(product.previous_client_stock)
                        if product.previous_client_stock is not None
                        else None,
                        sales_quantity=product.sales_quantity,
                        loss_quantity=product.loss_quantity,
                         shelf_price=float(product.shelf_price) if product.shelf_price is not None else None,
                        next_qty=product.next_quantity,
                        previous_quantity=(
                            int(prev.previous_quantity) if prev and prev.previous_quantity is not None else None
                        ),
                        previous_visited_at=prev.previous_visited_at if prev else None,
                    )
                )

            visit_payloads.append(
                InventoryVisitWithHistoryResponse(
                    ticket_id=visit.ticket_id,
                    visit_id=visit.id,
                    visited_at=visit.visited_at,
                    cost_center_id=visit.cost_center_id,
                    products=product_payloads,
                )
            )

        return InventoryVisitHistoryPaginatedResponse(
            items=visit_payloads,
            total=data["total"],
            page=data["page"],
            page_size=data["page_size"],
            total_pages=data["total_pages"],
        )
    
