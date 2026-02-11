from datetime import datetime
import logging
from typing import List, Optional
from fastapi import Query
from app.controller.tickets_controller.tickets_controller import (
    close_ticket_controller,
    process_sales_controller,
    search_tickets_by_term_controller,
    register_inventory_visit_controller,
    update_inventory_visit_controller,
    list_inventory_visits_controller,
    get_ticket_cycle_products_controller,
    get_cost_center_product_visits_controller,
    get_previous_approved_ticket_controller,
    get_cost_center_latest_visits_controller,
    get_ticket_visit_summary_controller,
    get_cost_center_last_visit_next_qty_controller,
    get_open_reservations_controller,
)
from app.schemas.list_all_schemas.list_all_responses import AllTicketsResponse
from app.schemas.products_schemas.product_price_schema import UnitPricePayload
from app.schemas.tickets_schemas.tickets_schemas import TicketProductUpdateDTO, TicketRegisterSales
from app.schemas.tickets_schemas.inventory_visit_schema import (
    InventoryVisitCreate,
    InventoryVisitUpdate,
    InventoryVisitResponse,
    InventoryVisitHistoryPaginatedResponse,
    TicketCycleProductsResponse,
    CostCenterProductVisitsResponse,
    CostCenterLatestVisitsResponse,
    TicketVisitSummaryResponse,
    LastVisitNextQtyResponse,
    ReservationsResponse,
)

from app.service.tickets_service.ticket_lifecycle_service import TicketLifecycleService
from app.service.tickets_service.ticket_product_service import TicketProductService
from app.service.tickets_service.tickets_service import TicketService
from . import *
from app.middleware.auth_handler import get_current_user

router = APIRouter(redirect_slashes=False)
logger = logging.getLogger(__name__)

@router.get("/tickets", include_in_schema=False)
@router.get("/tickets/", response_model=AllTicketsResponse, tags=["Tickets"])
def get_tickets( page: int = Query(1, ge=1),db: Session = Depends(get_db), start_date: Optional[datetime] = Query(None), end_date: Optional[datetime] = Query(None)):
    return list_tickets(page, db, start_date=start_date, end_date=end_date)

@router.post("/tickets", include_in_schema=False)
@router.post("/tickets/", response_model=TicketResponse, tags=["Tickets"])
def create_new_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        ticket_data.created_by = user['id']
        result = create_ticket(ticket_data, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/tickets/{ticket_id}/", include_in_schema=False)
@router.put("/tickets/{ticket_id}", response_model=TicketResponse, tags=["Tickets"])
def update_ticket(ticket_id: int, ticket_data: TicketResponse, db: Session = Depends(get_db)):
    return edit_ticket(ticket_id, ticket_data, db)

@router.delete("/tickets/{ticket_id}/", include_in_schema=False)
@router.delete("/tickets/{ticket_id}", tags=["Tickets"])
def remove_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return delete_ticket(ticket_id, db)


@router.get("/tickets/search/", include_in_schema=False)
@router.get("/tickets/search", response_model=AllTicketsResponse, tags=["Tickets"])
def search_tickets_any_route(
    term: str,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    tickets = search_tickets_by_term_controller( term,page,db, start_date=start_date, end_date=end_date)
    return tickets


@router.get("/tickets/{ticket_id}/products", include_in_schema=False)
@router.get("/tickets/{ticket_id}/products/", response_model=List[int], tags=["Tickets"])
def get_products_for_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return TicketProductService.get_products_for_ticket(ticket_id, db)

@router.get("/tickets/{ticket_id}/previous-approved", include_in_schema=False)
@router.get("/tickets/{ticket_id}/previous-approved/", response_model=TicketResponse, tags=["Tickets"])
def get_previous_approved_ticket_route(ticket_id: int, db: Session = Depends(get_db)):
    return get_previous_approved_ticket_controller(ticket_id, db)



@router.post("/tickets/products", include_in_schema=False)
@router.post("/tickets/products/", response_model=TicketProductResponse, tags=["Tickets"])
def add_product_to_ticket_route(product_data: TicketProductCreate, db: Session = Depends(get_db)):
    return TicketProductService.add_product(product_data, db)

@router.delete("/tickets/products/{ticket_product_id}/", include_in_schema=False)
@router.delete("/tickets/products/{ticket_product_id}", tags=["Tickets"])
def remove_product_from_ticket_route(ticket_product_id: int, db: Session = Depends(get_db)):
    return TicketProductService.remove_product( db,ticket_product_id)

@router.post("/tickets/{id}/close/", include_in_schema=False)
@router.post("/tickets/{id}/close", tags=["Tickets"])
def close_ticket_product(id: int, db: Session = Depends(get_db)):
    return close_ticket_controller( id, db)

@router.post("/tickets/update-sales/", include_in_schema=False)
@router.post("/tickets/update-sales", response_model=TicketRegisterSales, tags=["Tickets"])
def update_ticket_products_and_create_movements(
    ticket: TicketRegisterSales,
    db: Session = Depends(get_db)
):
    return process_sales_controller(ticket, db)

@router.patch("/products/{ticket_product_id}/unit-price/", include_in_schema=False)
@router.patch("/products/{ticket_product_id}/unit-price", tags=["Tickets"])
def set_unit_price(ticket_product_id: int, body: UnitPricePayload, db: Session = Depends(get_db)):
    tp = TicketService.set_ticket_product_unit_price(db, ticket_product_id, body.unit_price)
    if not tp:
        raise HTTPException(404, "TicketProduct não encontrado")
    return {
        "id": tp.id,
        "ticket_id": tp.ticket_id,
        "product_id": tp.product_id,
        "unit_price": float(tp.unit_price) if tp.unit_price is not None else None,
    }


@router.post("/{ticket_id}/approve/" , include_in_schema=False)
@router.post("/{ticket_id}/approve" , tags=["Tickets"])
def approve_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db)):
    """
    Aprova o ticket e transfere o estoque do inventário para o cliente.
    """
    try:
        ticket = TicketLifecycleService.approve_ticket(ticket_id, db)
        return ticket  # Se tiver um schema pydantic, você pode usar response_model aqui

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao aprovar ticket: {str(e)}")
    
@router.get("/last-approved/" , include_in_schema=False)
@router.get("/last-approved" , response_model=TicketResponse, tags=["Tickets"]) 
def get_last_approved_ticket_id(
    cost_center_id: int = Query(..., ge=1),
    product_id: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    return TicketLifecycleService.get_last_approved_ticket_id_service(db, cost_center_id, product_id)

 
    
    

@router.put("/{ticket_id}/products/{product_id}/", include_in_schema=False)
@router.put("/{ticket_id}/products/{product_id}", tags=["Tickets"])
def update_ticket_product(
    ticket_id: int,
    product_id: int,
    payload: TicketProductUpdateDTO,
    db: Session = Depends(get_db),
):
    try:
        payload.ensure_not_empty()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    updates = payload.model_dump(exclude_none=True)
    updated = TicketProductService.update_ticket_product_service(
        db, ticket_id=ticket_id, product_id=product_id, updates=updates
    )

    return {
        "ticket_id": ticket_id,
        "product_id": product_id,
        "sent_quantity": int(updated.sent_quantity),
        "unit_price": str(updated.unit_price) if updated.unit_price is not None else None,
        "entry_price": str(updated.entry_price) if updated.entry_price is not None else None,
        "message": "Produto do ticket atualizado com sucesso.",
    }


@router.post("/tickets/{ticket_id}/visits", include_in_schema=False)
@router.post(
    "/tickets/{ticket_id}/visits/",
    response_model=InventoryVisitResponse,
    tags=["Visits"],
)
def register_inventory_visit_route(
    ticket_id: int,
    visit_data: InventoryVisitCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    recorded_by = user.get("id") if isinstance(user, dict) else None
    logger.info(
        "POST /tickets/%s/visits payload=%s recorded_by=%s",
        ticket_id,
        visit_data.model_dump(),
        recorded_by,
    )
    return register_inventory_visit_controller(ticket_id, visit_data, db, recorded_by)

@router.put("/tickets/{ticket_id}/visits/{visit_id}", include_in_schema=False)
@router.put(
    "/tickets/{ticket_id}/visits/{visit_id}/",
    response_model=InventoryVisitResponse,
    tags=["Visits"],
)
def update_inventory_visit_route(
    ticket_id: int,
    visit_id: int,
    visit_data: InventoryVisitUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    current_user_id = user.get("id") if isinstance(user, dict) else None
    return update_inventory_visit_controller(ticket_id, visit_id, visit_data, db, current_user_id)


@router.get("/tickets/{ticket_id}/visits", include_in_schema=False)
@router.get(
    "/tickets/{ticket_id}/visits/",
    response_model=List[InventoryVisitResponse],
    tags=["Tickets"],
)
def list_inventory_visits_route(
    ticket_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    current_user_id = user.get("id") if isinstance(user, dict) else None
    return list_inventory_visits_controller(ticket_id, db, current_user_id)

@router.get("/tickets/{ticket_id}/cycle-products", include_in_schema=False)
@router.get(
    "/tickets/{ticket_id}/cycle-products/",
    response_model=TicketCycleProductsResponse,
    tags=["Tickets"],
)
def get_ticket_cycle_products_route(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    return get_ticket_cycle_products_controller(ticket_id, db)

@router.get("/tickets/{ticket_id}/visit-summary", include_in_schema=False)
@router.get(
    "/tickets/{ticket_id}/visit-summary/",
    response_model=TicketVisitSummaryResponse,
    tags=["Visits"],
)
def get_ticket_visit_summary_route(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    return get_ticket_visit_summary_controller(ticket_id, db)

@router.get("/cost-centers/{cost_center_id}/visits/latest-next-qty", include_in_schema=False)
@router.get(
    "/cost-centers/{cost_center_id}/visits/latest-next-qty/",
    response_model=LastVisitNextQtyResponse,
    tags=["Visits"],
)
def get_cost_center_last_visit_next_qty_route(
    cost_center_id: int,
    db: Session = Depends(get_db),
):
    return get_cost_center_last_visit_next_qty_controller(cost_center_id, db)

@router.get("/open/reservations", include_in_schema=False)
@router.get(
    "/open/reservations/",
    response_model=ReservationsResponse,
    tags=["Tickets"],
)
def get_open_reservations_route(
    product_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db),
):
    return get_open_reservations_controller(product_ids, db)

@router.get("/cost-centers/{cost_center_id}/visits/latest", include_in_schema=False)
@router.get(
    "/cost-centers/{cost_center_id}/visits/latest/",
    response_model=CostCenterLatestVisitsResponse,
    tags=["Visits"],
)
def get_cost_center_latest_visits_route(
    cost_center_id: int,
    limit: int = Query(2, ge=1, le=20),
    ticket_id: Optional[int] = Query(None, ge=1),
    db: Session = Depends(get_db),
):
    return get_cost_center_latest_visits_controller(cost_center_id, limit, ticket_id, db)

@router.get("/cost-centers/{cost_center_id}/product-visits", include_in_schema=False)
@router.get(
    "/cost-centers/{cost_center_id}/product-visits/",
    response_model=CostCenterProductVisitsResponse,
    tags=["Visits"],
)
def get_cost_center_product_visits_route(
    cost_center_id: int,
    product_ids: Optional[List[int]] = Query(None),
    db: Session = Depends(get_db),
):
    return get_cost_center_product_visits_controller(cost_center_id, product_ids, db)


@router.get("/visits", include_in_schema=False)
@router.get(
    "/visits/",
    response_model=InventoryVisitHistoryPaginatedResponse,
    tags=["Visits"],
)
def list_all_inventory_visits_route(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return TicketService.list_all_inventory_visits(db, page, page_size)
