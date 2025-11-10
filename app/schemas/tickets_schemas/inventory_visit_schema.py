from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.tickets_schemas.cost_center_schemas import CostCenterResponse


class InventoryVisitProductBase(BaseModel):
    product_id: int
    stock_quantity: int = Field(ge=0)
    sales_quantity: int = Field(default=0, ge=0)
    loss_quantity: int = Field(default=0, ge=0)


class InventoryVisitProductCreate(InventoryVisitProductBase):
    pass


class InventoryVisitProductResponse(InventoryVisitProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class InventoryVisitBase(BaseModel):
    visited_at: Optional[datetime] = None
    total_stock_quantity: Optional[int] = None
    notes: Optional[str] = None


class InventoryVisitCreate(InventoryVisitBase):
    products: List[InventoryVisitProductCreate] = Field(..., min_length=1)


class InventoryVisitResponse(InventoryVisitBase):
    id: int
    ticket_id: Optional[int] = None
    cost_center_id: int
    recorded_by: Optional[int] = None
    cost_center: Optional[CostCenterResponse] = None
    products: List[InventoryVisitProductResponse] = []

    model_config = ConfigDict(from_attributes=True)
