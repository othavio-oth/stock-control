from datetime import datetime, timedelta, date, timezone
from typing import Optional, List
import re
from fastapi import HTTPException
from pytest import Session
from sqlalchemy import and_, func, or_, text
from sqlalchemy.orm import joinedload
from app.models.product import Product
from app.models.stockMovement import (
    InventoryStock,
    InventoryVisit,
    InventoryVisitProduct,
    MovementType,
    StockMovement,
    ClientSalesHistory,
    ClientLossHistory,
)
from app.models.user import User, Role, UserRole
from app.repository.stock.stock_movement_repository import process_stock_movement
from app.repository.stock.client_stock_repository import get_client_stock_by_cost_center
from app.repository.tickets.tickets_repository import (
    create_ticket,
    get_all_tickets,
    get_last_approved_ticket_id_for_cc_product,
    get_ticket_by_id,
    search_tickets_any,
    update_ticket,
    delete_ticket,
    add_product_to_ticket,
    get_products_by_ticket,
    get_products_ticket_by_id,
    get_ticket_products,
    remove_product_from_ticket,
    update_ticket_product,
    update_ticket_product_unit_price,
    create_inventory_visit_record,
    update_inventory_visit_record,
    list_inventory_visits_by_ticket,
    list_all_inventory_visits_paginated,
    get_previous_inventory_snapshot,
    get_previous_approved_ticket_for_cost_center,
)
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

        if TicketService._user_is_admin(db, current_user_id):
            return visits
        return [
            visit for visit in visits
            if visit.recorded_by == current_user_id
        ]

    @staticmethod
    def get_ticket_cycle_products(db: Session, ticket_id: int) -> TicketCycleProductsResponse:
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket nuo encontrado")

        product_ids = list({tp.product_id for tp in ticket.products})
        visits_by_product = TicketService._collect_visits_by_product(
            db,
            cost_center_id=ticket.cost_center_id,
            product_ids=product_ids,
            allowed_ticket_ids=TicketService._get_allowed_ticket_ids(db, ticket),
        )
        seen_products: set[int] = set()
        products_payload: list[ProductCycleTimelineResponse] = []
        for tp in ticket.products:
            if tp.product_id in seen_products:
                continue
            seen_products.add(tp.product_id)

            visit_entries = visits_by_product.get(tp.product_id, [])

            current_block = TicketService._build_cycle_block(visit_entries[0]) if len(visit_entries) > 0 else None
            previous_block = TicketService._build_cycle_block(visit_entries[1]) if len(visit_entries) > 1 else None
            previous2_block = TicketService._build_cycle_block(visit_entries[2]) if len(visit_entries) > 2 else None

            products_payload.append(
                ProductCycleTimelineResponse(
                    product_id=tp.product_id,
                    name=getattr(tp.product, "name", None),
                    custom_id=getattr(tp.product, "custom_id", None),
                    previous2=previous2_block,
                    previous=previous_block,
                    current=current_block,
                )
            )

        return TicketCycleProductsResponse(
            ticket_id=ticket.id,
            cost_center_id=ticket.cost_center_id,
            products=products_payload,
        )

    @staticmethod
    def get_cost_center_product_visits(
        db: Session,
        *,
        cost_center_id: int,
        product_ids: Optional[List[int]] = None,
    ) -> CostCenterProductVisitsResponse:
        if product_ids:
            filtered_ids = sorted({int(pid) for pid in product_ids})
        else:
            filtered_ids = [
                row.product_id
                for row in (
                    db.query(InventoryVisitProduct.product_id)
                    .join(InventoryVisit, InventoryVisit.id == InventoryVisitProduct.inventory_visit_id)
                    .filter(InventoryVisit.cost_center_id == cost_center_id)
                    .distinct()
                    .all()
                )
            ]

        if not filtered_ids:
            return CostCenterProductVisitsResponse(cost_center_id=cost_center_id, visits=[])

        products = (
            db.query(Product.id, Product.name, Product.custom_id)
            .filter(Product.id.in_(filtered_ids))
            .all()
        )
        product_meta = {
            row.id: {"name": row.name, "custom_id": row.custom_id}
            for row in products
        }
        if not product_meta:
            return CostCenterProductVisitsResponse(cost_center_id=cost_center_id, visits=[])

        visits_by_product = TicketService._collect_visits_by_product(
            db,
            cost_center_id=cost_center_id,
            product_ids=list(product_meta.keys()),
        )

        visits_payload: list[ProductVisitSnapshot] = []
        for product_id, meta in product_meta.items():
            visit_entries = visits_by_product.get(product_id, [])
            for visit_row in visit_entries:
                visits_payload.append(
                    ProductVisitSnapshot(
                        product_id=product_id,
                        name=meta.get("name"),
                        custom_id=meta.get("custom_id"),
                        ticket_id=getattr(visit_row, "ticket_id", None),
                        visited_at=date_to_str(getattr(visit_row, "visited_at", None)),
                        quantity_ordered=(
                            int(visit_row.quantity_ordered)
                            if getattr(visit_row, "quantity_ordered", None) is not None
                            else None
                        ),
                        shelf_price=(
                            float(visit_row.shelf_price)
                            if getattr(visit_row, "shelf_price", None) is not None
                            else None
                        ),
                        stock_quantity=(
                            int(visit_row.stock_quantity)
                            if getattr(visit_row, "stock_quantity", None) is not None
                            else None
                        ),
                        loss_quantity=(
                            int(visit_row.loss_quantity)
                            if getattr(visit_row, "loss_quantity", None) is not None
                            else None
                        ),
                        next_qty=(
                            int(visit_row.next_quantity)
                            if getattr(visit_row, "next_quantity", None) is not None
                            else None
                        ),
                    )
                )

        return CostCenterProductVisitsResponse(
            cost_center_id=cost_center_id,
            visits=visits_payload,
        )

    @staticmethod
    def get_cost_center_latest_visits(
        db: Session,
        *,
        cost_center_id: int,
        limit: int = 2,
        ticket_id: Optional[int] = None,
    ) -> CostCenterLatestVisitsResponse:
        effective_limit = limit if isinstance(limit, int) and limit > 0 else 2
        base_query = (
            db.query(InventoryVisit)
            .options(
                joinedload(InventoryVisit.products).joinedload(InventoryVisitProduct.product),
            )
            .filter(InventoryVisit.cost_center_id == cost_center_id)
            .order_by(InventoryVisit.visited_at.desc(), InventoryVisit.id.desc())
        )

        visits: list[InventoryVisit] = []
        if ticket_id:
            visits_query = base_query.filter(
                InventoryVisit.ticket_id.isnot(None),
                InventoryVisit.ticket_id <= ticket_id,
            )
            if effective_limit > 0:
                visits_query = visits_query.limit(effective_limit)
            visits = visits_query.all()
        else:
            visits_query = base_query
            if effective_limit > 0:
                visits_query = visits_query.limit(effective_limit)
            visits = visits_query.all()

        if not visits:
            return CostCenterLatestVisitsResponse(cost_center_id=cost_center_id, visits=[])

        ticket_ids = {visit.ticket_id for visit in visits if visit.ticket_id}
        ticket_product_rows = (
            db.query(
                TicketProduct.ticket_id.label("ticket_id"),
                TicketProduct.product_id.label("product_id"),
                TicketProduct.quantity_ordered.label("quantity_ordered"),
            )
            .filter(TicketProduct.ticket_id.in_(ticket_ids))
            .all()
            if ticket_ids
            else []
        )
        quantity_map = {
            (row.ticket_id, row.product_id): int(row.quantity_ordered) if row.quantity_ordered is not None else None
            for row in ticket_product_rows
        }

        visit_payloads: list[CostCenterVisitSnapshot] = []
        for visit in visits:
            products_payload: list[VisitProductSnapshot] = []
            for product_entry in visit.products or []:
                products_payload.append(
                    VisitProductSnapshot(
                        product_id=product_entry.product_id,
                        name=getattr(product_entry.product, "name", None),
                        custom_id=getattr(product_entry.product, "custom_id", None),
                        quantity_ordered=quantity_map.get((visit.ticket_id, product_entry.product_id)),
                        stock_quantity=product_entry.stock_quantity,
                        loss_quantity=product_entry.loss_quantity,
                        shelf_price=float(product_entry.shelf_price) if product_entry.shelf_price is not None else None,
                        next_qty=product_entry.next_quantity,
                    )
                )

            visit_payloads.append(
                CostCenterVisitSnapshot(
                    visit_id=visit.id,
                    ticket_id=visit.ticket_id,
                    visited_at=date_to_str(visit.visited_at),
                    total_stock_quantity=visit.total_stock_quantity,
                    products=products_payload,
                )
            )

        return CostCenterLatestVisitsResponse(
            cost_center_id=cost_center_id,
            visits=visit_payloads,
        )

    @staticmethod
    def get_ticket_visit_summary(db: Session, ticket_id: int) -> TicketVisitSummaryResponse:
        ticket = get_ticket_by_id(db, ticket_id)
        if not ticket:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Ticket nao encontrado.")

        cutoff_dt = None
        if getattr(ticket, "order_date", None):
            cutoff_dt = datetime.combine(ticket.order_date, datetime.max.time())
        elif getattr(ticket, "approved_at", None):
            cutoff_dt = ticket.approved_at
        elif getattr(ticket, "created_at", None):
            cutoff_dt = ticket.created_at
        else:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Data de referencia do ticket nao encontrada.")

        # Normaliza cutoff para evitar comparações inconsistentes de timezone
        if cutoff_dt:
            if cutoff_dt.tzinfo is None:
                cutoff_dt = cutoff_dt.replace(tzinfo=timezone.utc)
            else:
                cutoff_dt = cutoff_dt.astimezone(timezone.utc)

        rows = db.execute(
            text(
                """
                WITH ranked AS (
                    SELECT
                        ivp.product_id,
                        iv.visited_at,
                        ivp.loss_quantity,
                        ivp.sales_quantity,
                        ivp.stock_quantity,
                        ivp.next_quantity,
                        tp.quantity_ordered,
                        ROW_NUMBER() OVER (
                            PARTITION BY ivp.product_id
                            ORDER BY iv.visited_at DESC, iv.id DESC
                        ) AS rn
                    FROM inventory_visits iv
                    JOIN inventory_visit_products ivp ON ivp.inventory_visit_id = iv.id
                    LEFT JOIN ticket_products tp
                        ON tp.ticket_id = iv.ticket_id
                        AND tp.product_id = ivp.product_id
                    WHERE iv.cost_center_id = :cost_center_id
                      AND iv.visited_at < :cutoff
                )
                SELECT
                    product_id,
                    MAX(CASE WHEN rn = 1 THEN loss_quantity END)  AS loss_last,
                    MAX(CASE WHEN rn = 2 THEN loss_quantity END)  AS loss_prev,
                    MAX(CASE WHEN rn = 1 THEN sales_quantity END) AS sales_last,
                    MAX(CASE WHEN rn = 2 THEN sales_quantity END) AS sales_prev,
                    MAX(CASE WHEN rn = 1 THEN stock_quantity END) AS stock_last,
                    MAX(CASE WHEN rn = 2 THEN stock_quantity END) AS stock_prev,
                    MAX(CASE WHEN rn = 1 THEN next_quantity END) AS next_qty,
                    MAX(CASE WHEN rn = 1 THEN quantity_ordered END) AS order_last,
                    MAX(CASE WHEN rn = 2 THEN quantity_ordered END) AS order_prev,
                    MAX(CASE WHEN rn = 2 THEN visited_at END) AS order_prev_date
                FROM ranked
                WHERE rn <= 2
                GROUP BY product_id
                ORDER BY product_id
                """
            ),
            {
                "ticket_id": ticket_id,
                "cost_center_id": ticket.cost_center_id,
                "cutoff": cutoff_dt,
            },
        ).fetchall()

        items = []
        approved_tickets = (
            db.query(Ticket)
            .filter(
                Ticket.cost_center_id == ticket.cost_center_id,
                Ticket.approved_at.isnot(None),
            )
            .order_by(Ticket.approved_at.desc(), Ticket.id.desc())
            .limit(2)
            .all()
        )
        ticket_order_date = date_to_str(
            approved_tickets[0].order_date
            or approved_tickets[0].approved_at
            or approved_tickets[0].created_at
        ) if approved_tickets else None
        previous_ticket_date = date_to_str(
            approved_tickets[1].order_date
            or approved_tickets[1].approved_at
            or approved_tickets[1].created_at
        ) if len(approved_tickets) > 1 else None
        for row in rows:
            items.append(
                TicketVisitSummaryItem(
                    product_id=row.product_id,
                    loss_last=row.loss_last,
                    loss_prev=row.loss_prev,
                    sales_last=row.sales_last,
                    sales_prev=row.sales_prev,
                    stock_last=row.stock_last,
                    stock_prev=row.stock_prev,
                    next_qty=row.next_qty,
                    order_last=row.order_last,
                    order_prev=row.order_prev,
                    order_last_date=ticket_order_date,
                    order_prev_date=previous_ticket_date,
                )
            )

        return TicketVisitSummaryResponse(ticket_id=ticket_id, items=items)

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
    def get_open_reservations(
        db: Session,
        product_ids: Optional[List[int]] = None,
    ) -> ReservationsResponse:
        statuses = ["open", "pending"]

        base_query = (
            db.query(
                TicketProduct.product_id.label("product_id"),
                TicketProduct.ticket_id.label("ticket_id"),
                Ticket.cost_center_id.label("cost_center_id"),
                TicketProduct.quantity_ordered.label("quantity"),
            )
            .join(Ticket, TicketProduct.ticket_id == Ticket.id)
            .filter(Ticket.status.in_(statuses))
        )

        if product_ids:
            normalized_ids = sorted({int(pid) for pid in product_ids})
            if normalized_ids:
                base_query = base_query.filter(TicketProduct.product_id.in_(normalized_ids))

        detail_rows = base_query.all()

        if not detail_rows:
            return ReservationsResponse(generated_at=datetime.utcnow(), items=[])

        agg: dict[int, dict] = {}
        for row in detail_rows:
            pid = row.product_id
            qty = int(row.quantity or 0)
            entry = agg.setdefault(pid, {"reserved_qty": 0, "tickets": []})
            entry["reserved_qty"] += qty
            entry["tickets"].append(
                ReservationTicketItem(
                    ticket_id=row.ticket_id,
                    cost_center_id=row.cost_center_id,
                    quantity=qty,
                )
            )

        items = [
            ReservationItem(
                product_id=pid,
                reserved_qty=data["reserved_qty"],
                tickets=data["tickets"],
            )
            for pid, data in sorted(agg.items())
        ]

        return ReservationsResponse(
            generated_at=datetime.utcnow(),
            items=items,
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

    @staticmethod
    def update_ticket_product_service(db: Session, ticket_id: int, product_id: int, updates: dict):
        return update_ticket_product(db, ticket_id, product_id, updates)
