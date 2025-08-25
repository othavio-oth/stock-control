from datetime import datetime
from fastapi import Query
from app.controller.tickets_controller.tickets_controller import close_ticket_controller, process_sales_controller, search_tickets_by_term_controller
from app.schemas.list_all_schemas.list_all_responses import AllTicketsResponse
from app.schemas.products_schemas.product_price_schema import UnitPricePayload
from app.schemas.products_schemas.sales_schemas import MultiCycleAnalysisResponse, ProductHistoryAnalysis
from app.schemas.tickets_schemas.tickets_schemas import TicketProductUpdateDTO, TicketRegisterSales
from app.service.tickets_service.ticket_recommendations_service import get_daily_sales_avg_for_last_cycles, get_daily_sales_avg_for_ticket
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

@router.get("/{ticket_id}/average-daily-sales")
def average_daily_sales_endpoint(
    ticket_id: int,
    evaluation_time: Optional[str] = Query(
        default=None,
        description="Momento de referência (ISO 8601). Ex.: 2025-08-18T14:30:00"
    ),
    db: Session = Depends(get_db),
):
    """
    Retorna, para cada produto do ticket, a média de vendas por hora e por dia comercial (07–20),
    calculada do dia seguinte (07:00) ao último ticket aprovado que continha o produto até
    `evaluation_time` (ou agora, se omitido).
    """
    try:
        eval_dt: Optional[datetime] = None
        if evaluation_time:
            try:
                eval_dt = datetime.fromisoformat(evaluation_time)
            except ValueError:
                raise HTTPException(status_code=400, detail="evaluation_time inválido. Use ISO 8601 (ex.: 2025-08-18T14:30:00)")

        data = get_daily_sales_avg_for_ticket(db=db, ticket_id=ticket_id, evaluation_time=eval_dt)
        return {"ticket_id": ticket_id, "items": data}
    except ValueError as e:
        # Erros de validação do service (ex.: ticket não encontrado)
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular médias: {str(e)}")
    
    
    
@router.get("/{ticket_id}/analysis/history", response_model=MultiCycleAnalysisResponse)
def get_analysis_history(
    ticket_id: int,
    max_cycles: int = Query(8, ge=1, le=50),
    db: Session = Depends(get_db),
    user = Depends(get_current_user),  # se houver auth
):
    raw = get_daily_sales_avg_for_last_cycles(db, ticket_id, max_cycles=max_cycles)

    items: List[ProductHistoryAnalysis] = []
    for product_id, cycles in raw.items():
        # 'cycles' já é uma lista de dicts com as chaves exigidas em CycleAnalysis
        items.append(ProductHistoryAnalysis(product_id=product_id, cycles=cycles))

    return MultiCycleAnalysisResponse(
        ticket_id=ticket_id,
        max_cycles=max_cycles,
        items=items
    )
    

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

    updated = TicketService.update_ticket_product_service(
        db, ticket_id=ticket_id, product_id=product_id, updates=payload.model_dump()
    )

    return {
        "ticket_id": ticket_id,
        "product_id": product_id,
        "quantity_ordered": int(updated.quantity_ordered),
        "unit_price": str(updated.unit_price) if updated.unit_price is not None else None,
        "entry_price": str(updated.entry_price) if updated.entry_price is not None else None,
        "message": "Produto do ticket atualizado com sucesso.",
    }