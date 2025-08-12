from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.middleware.db import get_db
from app.schemas.products_schemas.product_price_schema import ProductPriceHistoryCreate, ProductPriceHistoryUpdate
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

@router.get("/entity-price")
def get_entity_price_endpoint(
    product_id: int,
    retail_chain_id: Optional[int] = None,
    cost_center_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    try:
        result = ProductPriceHistoryService.get_price_for_entity_service(
            db,
            product_id=product_id,
            retail_chain_id=retail_chain_id,
            cost_center_id=cost_center_id
        )
        if not result:
            raise HTTPException(status_code=404, detail="Price not found for this entity")
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def get_current_prices_endpoint( db: Session = Depends(get_db)):
    return ProductPriceHistoryService.get_all_current_prices_service(db)