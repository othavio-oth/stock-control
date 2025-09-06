# app/api/sales.py
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from sqlalchemy.orm import Session

from app.middleware.db import get_db
from app.schemas.stock_schemas.stock_movement_schema import RegisterClientSalesDTO
from app.service.products_service.products_sales_service import ProductSalesService


router = APIRouter( tags=["Sales"],redirect_slashes=False)

@router.post("/register/", include_in_schema=False)
@router.post("/register")
def register_client_sales_simple(payload: RegisterClientSalesDTO, db: Session = Depends(get_db)):
    try:
        result = ProductSalesService.register_client_sales_simple(db, payload)
        return result
    except ValueError as e:
        # erros de regra de negócio (ex: estoque insuficiente, data futura, etc.)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao registrar venda")
