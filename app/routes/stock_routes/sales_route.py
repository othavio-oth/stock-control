# app/api/sales.py
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session

from app.middleware.db import get_db
from app.schemas.stock_schemas.stock_movement_schema import ClientSalesAnchoredDTO
from app.service.products_service.products_sales_service import ProductSalesService


router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/tickets/{ticket_id}/anchored")
def post_sales_anchored(
    ticket_id: int,
    body: ClientSalesAnchoredDTO,
    db: Session = Depends(get_db),
):
    try:
        body.ticket_id = ticket_id  # garante alinhamento com o path param
        return ProductSalesService.register_client_sales_anchored_to_ticket(db, body)
    except ValueError as e:
        msg = str(e)
        if "Ticket" in msg and "não foi encontrado" in msg:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=msg)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=msg)
