from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.middleware.db import get_db
from app.schemas.products_schemas.shelf_price_schema import (
    ShelfPriceCreate,
    ShelfPriceResponse,
    ShelfPriceUpdate,
)
from app.service.products_service.shelf_price_service import ShelfPriceService

router = APIRouter(tags=["shelf_prices"], redirect_slashes=False)


@router.post("", include_in_schema=False)
@router.post("/", response_model=ShelfPriceResponse)
def create_shelf_price_endpoint(data: ShelfPriceCreate, db: Session = Depends(get_db)):
    try:
        return ShelfPriceService.create(db, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", include_in_schema=False)
@router.get("/", response_model=List[ShelfPriceResponse])
def list_shelf_prices_endpoint(
    product_id: Optional[int] = Query(None),
    cost_center_id: Optional[int] = Query(None),
    retail_chain_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
):
    return ShelfPriceService.list(
        db,
        product_id=product_id,
        cost_center_id=cost_center_id,
        retail_chain_id=retail_chain_id,
    )


@router.get("/{shelf_price_id}", response_model=ShelfPriceResponse)
def get_shelf_price_endpoint(shelf_price_id: int, db: Session = Depends(get_db)):
    shelf_price = ShelfPriceService.get_by_id(db, shelf_price_id)
    if not shelf_price:
        raise HTTPException(status_code=404, detail="Shelf price not found")
    return shelf_price


@router.patch("/{shelf_price_id}", response_model=ShelfPriceResponse)
def update_shelf_price_endpoint(
    shelf_price_id: int,
    data: ShelfPriceUpdate,
    db: Session = Depends(get_db),
):
    try:
        shelf_price = ShelfPriceService.update(db, shelf_price_id, data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    if not shelf_price:
        raise HTTPException(status_code=404, detail="Shelf price not found")
    return shelf_price


@router.delete("/{shelf_price_id}")
def delete_shelf_price_endpoint(shelf_price_id: int, db: Session = Depends(get_db)):
    deleted = ShelfPriceService.delete(db, shelf_price_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shelf price not found")
    return {"message": "Shelf price deleted successfully"}
