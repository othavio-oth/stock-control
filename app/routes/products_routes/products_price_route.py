from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.middleware.db import get_db
from app.schemas.products_schemas.product_price_schema import ProductCurrentPriceResponse, ProductPriceHistoryCreate, ProductPriceHistoryUpdate
from app.service.products_service.products_price_service import ProductPriceHistoryService

router = APIRouter( tags=["prices"])

@router.post("/")
def create_price_endpoint(data: ProductPriceHistoryCreate, db: Session = Depends(get_db)):
    try:
        return ProductPriceHistoryService.create_price_history_service(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/products/{product_id}")
def get_current_prices_endpoint(product_id: int, db: Session = Depends(get_db)):
    return ProductPriceHistoryService.get_current_prices_service_by_product(db, product_id)

@router.patch("/{price_id}")
def update_price_endpoint(price_id: int, data: ProductPriceHistoryUpdate, db: Session = Depends(get_db)):
    result = ProductPriceHistoryService.update_price_servicejj(db, price_id, data)
    if not result:
        raise HTTPException(status_code=404, detail="Price history not found")
    return result

@router.delete("/{price_id}")
def delete_price_endpoint(price_id: int, db: Session = Depends(get_db)):
    if not ProductPriceHistoryService.delete_price_service(db, price_id):
        raise HTTPException(status_code=404, detail="Price history not found")
    return {"message": "Price history deleted successfully"}


@router.get("/")
def get_current_prices_endpoint( db: Session = Depends(get_db)):
    return ProductPriceHistoryService.get_all_current_prices_service(db)

@router.get("/current-prices", response_model=List[ProductCurrentPriceResponse])
def get_current_prices_batch(
    cost_center_id: int = Query(..., description="ID do cost center"),
    ids: str = Query(..., description="Lista de product_ids separados por vírgula, ex: 1,2,3"),
    db: Session = Depends(get_db),
):
    try:
        product_ids = [int(x) for x in ids.split(",") if x.strip()]
    except ValueError:
        product_ids = []

    data = ProductPriceHistoryService.get_current_prices_batch_for_cost_center(
        db=db,
        product_ids=product_ids,
        cost_center_id=cost_center_id,
    )
    return data