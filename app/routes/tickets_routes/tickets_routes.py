from fastapi import Query
from app.controller.tickets_controller.tickets_controller import close_ticket_controller, process_sales_controller, search_tickets_by_term_controller
from app.schemas.list_all_schemas.list_all_responses import AllTicketsResponse
from app.schemas.products_schemas.product_price_schema import UnitPricePayload
from app.schemas.tickets_schemas.tickets_schemas import TicketRegisterSales
from app.service.tickets_service.tickets_service import TicketService
from . import *
from app.middleware.auth_handler import get_current_user

router = APIRouter()

@router.get("/tickets/", response_model=AllTicketsResponse, tags=["Tickets"])
def get_tickets( page: int = Query(1, ge=1),db: Session = Depends(get_db)):
    return list_tickets(page, db)

@router.post("/tickets/", response_model=TicketResponse, tags=["Tickets"])
def create_new_ticket(ticket_data: TicketCreate, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    try:
        ticket_data.created_by = user['id']
        result = create_ticket(ticket_data, db)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/tickets/{ticket_id}", response_model=TicketResponse, tags=["Tickets"])
def update_ticket(ticket_id: int, ticket_data: TicketResponse, db: Session = Depends(get_db)):
    return edit_ticket(ticket_id, ticket_data, db)

@router.delete("/tickets/{ticket_id}", tags=["Tickets"])
def remove_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return delete_ticket(ticket_id, db)


@router.get("/tickets/search", response_model=AllTicketsResponse, tags=["Tickets"])
def search_tickets_any_route(
    term: str,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    tickets = search_tickets_by_term_controller( term,page,db)
    return tickets


@router.get("/tickets/{ticket_id}/products/", response_model=List[int], tags=["Tickets"])
def get_products_for_ticket(ticket_id: int, db: Session = Depends(get_db)):
    return get_products_for_ticket_controller(ticket_id, db)

@router.get("/tickets/products/", response_model=List[TicketProductResponse], tags=["Tickets"])
def get_ticket_products_route(db: Session = Depends(get_db)):
    return get_ticket_products_controller(db)

@router.post("/tickets/products/", response_model=TicketProductResponse, tags=["Tickets"])
def add_product_to_ticket_route(product_data: TicketProductCreate, db: Session = Depends(get_db)):
    return add_product_to_ticket_controller(product_data, db)

@router.delete("/tickets/products/{ticket_product_id}", tags=["Tickets"])
def remove_product_from_ticket_route(ticket_product_id: int, db: Session = Depends(get_db)):
    return remove_product_from_ticket_controller(ticket_product_id, db)

@router.post("/tickets/{id}/close", tags=["Tickets"])
def close_ticket_product(id: int, db: Session = Depends(get_db)):
    return close_ticket_controller( id, db)

@router.post("/tickets/update-sales", response_model=TicketRegisterSales, tags=["Tickets"])
def update_ticket_products_and_create_movements(
    ticket: TicketRegisterSales,
    db: Session = Depends(get_db)
):
    return process_sales_controller(ticket, db)

@router.patch("/products/{ticket_product_id}/unit-price", tags=["Tickets"])
def set_unit_price(ticket_product_id: int, body: UnitPricePayload, db: Session = Depends(get_db)):
    tp = TicketService.set_ticket_product_unit_price(db, ticket_product_id, body.unit_price)
    if not tp:
        raise HTTPException(404, "TicketProduct não encontrado")
    return {"id": tp.id, "ticket_id": tp.ticket_id, "product_id": tp.product_id, "unit_price": float(tp.unit_price or 0)}


@router.post("/{ticket_id}/approve" , tags=["Tickets"])
def approve_ticket_endpoint(ticket_id: int, db: Session = Depends(get_db)):
    """
    Aprova o ticket e transfere o estoque do inventário para o cliente.
    """
    try:
        ticket = TicketService.approve_ticket(ticket_id, db)
        return ticket  # Se tiver um schema pydantic, você pode usar response_model aqui
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao aprovar ticket: {str(e)}")
    
@router.get("/last-approved" , tags=["Tickets"])
def get_last_approved_ticket_id(
    cost_center_id: int = Query(..., ge=1),
    product_id: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    return TicketService.get_last_approved_ticket_id_service(db, cost_center_id, product_id)