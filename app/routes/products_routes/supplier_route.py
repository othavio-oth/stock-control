from typing import List
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pytest import Session

from app.middleware.db import get_db
from app.schemas.products_schemas.supplier_schema import SupplierCreate, SupplierReponse, SupplierUpdate
from app.service.products_service.supplier_service import SupplierService


router = APIRouter( tags=["Suppliers"], prefix="/suppliers")

@router.get("", include_in_schema=False)
@router.get("/", response_model=List[SupplierReponse])
def get_suppliers(db: Session = Depends(get_db)):
    return SupplierService.list(db)

@router.post("", include_in_schema=False)
@router.post("/", response_model=SupplierReponse)
def create_new_supplier(supplier_data: SupplierCreate, db: Session = Depends(get_db)):
    try:
        return SupplierService.create(db, supplier_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{supplier_id}/", include_in_schema=False)
@router.put("/{supplier_id}", response_model=SupplierReponse )
def update_supplier(supplier_id: int, supplier_data: SupplierUpdate, db: Session = Depends(get_db)):
    try:
        return SupplierService.update(db, supplier_id, supplier_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{supplier_id}/", include_in_schema=False)
@router.delete("/{supplier_id}")
def remove_supplier(supplier_id: int, db: Session = Depends(get_db)):
    return SupplierService.delete(db,supplier_id )
