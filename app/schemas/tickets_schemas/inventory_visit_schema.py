from datetime import datetime, date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.tickets_schemas.cost_center_schemas import CostCenterResponse


class InventoryVisitProductBase(BaseModel):
    product_id: int
    stock_quantity: int = Field(ge=0)
    sales_quantity: int = Field(default=0, ge=0)
    loss_quantity: int = Field(default=0, ge=0)
    shelf_price: Optional[float] = Field(default=None, alias="shelfPrice", serialization_alias="shelfPrice")
    next_qty: Optional[int] = Field(default=None, ge=0, alias="nextQty", serialization_alias="nextQty")

    model_config = ConfigDict(populate_by_name=True)


class InventoryVisitProductCreate(InventoryVisitProductBase):
    pass


class InventoryVisitProductResponse(InventoryVisitProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class InventoryVisitProductWithHistoryResponse(InventoryVisitProductBase):
    previous_quantity: Optional[int] = None
    previous_visited_at: Optional[datetime] = None


class InventoryVisitBase(BaseModel):
    visited_at: Optional[datetime] = None
    total_stock_quantity: Optional[int] = None
    notes: Optional[str] = None


class InventoryVisitCreate(InventoryVisitBase):
    products: List[InventoryVisitProductCreate] = Field(..., min_length=1)


class InventoryVisitUpdate(InventoryVisitBase):
    products: Optional[List[InventoryVisitProductCreate]] = None


class InventoryVisitResponse(InventoryVisitBase):
    id: int
    ticket_id: Optional[int] = None
    cost_center_id: int
    recorded_by: Optional[int] = None
    cost_center: Optional[CostCenterResponse] = None
    products: List[InventoryVisitProductResponse] = []

    model_config = ConfigDict(from_attributes=True)


class InventoryVisitWithHistoryResponse(BaseModel):
    ticket_id: int
    visit_id: int
    visited_at: Optional[datetime] = None
    cost_center_id: int
    products: List[InventoryVisitProductWithHistoryResponse]


class InventoryVisitHistoryPaginatedResponse(BaseModel):
    items: List[InventoryVisitWithHistoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ProductCycleBlock(BaseModel):
    ticket_id: Optional[int] = None
    date: Optional[str] = None
    ordered: Optional[int] = None
    stock: Optional[int] = None
    loss: Optional[int] = None
    sales: Optional[int] = None


class ProductCycleTimelineResponse(BaseModel):
    product_id: int
    name: Optional[str] = None
    custom_id: Optional[str] = None
    previous2: Optional[ProductCycleBlock] = None
    previous: Optional[ProductCycleBlock] = None
    current: Optional[ProductCycleBlock] = None


class TicketCycleProductsResponse(BaseModel):
    ticket_id: int
    cost_center_id: int
    products: List[ProductCycleTimelineResponse]


class ProductVisitSnapshot(BaseModel):
    product_id: int
    name: Optional[str] = None
    custom_id: Optional[str] = None
    ticket_id: Optional[int] = None
    visited_at: Optional[str] = None
    quantity_ordered: Optional[int] = None
    stock_quantity: Optional[int] = None
    loss_quantity: Optional[int] = None
    shelf_price: Optional[float] = Field(default=None, alias="shelfPrice", serialization_alias="shelfPrice")
    next_qty: Optional[int] = Field(default=None, ge=0, alias="nextQty", serialization_alias="nextQty")
    model_config = ConfigDict(populate_by_name=True)


class CostCenterProductVisitsResponse(BaseModel):
    cost_center_id: int
    visits: List[ProductVisitSnapshot]


class VisitProductSnapshot(BaseModel):
    product_id: int
    name: Optional[str] = None
    custom_id: Optional[str] = None
    quantity_ordered: Optional[int] = None
    stock_quantity: Optional[int] = None
    loss_quantity: Optional[int] = None
    shelf_price: Optional[float] = Field(default=None, alias="shelfPrice", serialization_alias="shelfPrice")
    next_qty: Optional[int] = Field(default=None, ge=0, alias="nextQty", serialization_alias="nextQty")
    model_config = ConfigDict(populate_by_name=True)


class CostCenterVisitSnapshot(BaseModel):
    visit_id: int
    ticket_id: Optional[int] = None
    visited_at: Optional[str] = None
    total_stock_quantity: Optional[int] = None
    products: List[VisitProductSnapshot]


class CostCenterLatestVisitsResponse(BaseModel):
    cost_center_id: int
    visits: List[CostCenterVisitSnapshot]


class TicketVisitSummaryItem(BaseModel):
    product_id: int
    loss_last: Optional[int] = None
    loss_prev: Optional[int] = None
    sales_last: Optional[int] = None
    sales_prev: Optional[int] = None
    stock_last: Optional[int] = None
    stock_prev: Optional[int] = None
    next_qty: Optional[int] = Field(default=None, ge=0, alias="nextQty", serialization_alias="nextQty")
    order_last: Optional[int] = None
    order_prev: Optional[int] = None
    order_last_date: Optional[str] = None
    order_prev_date: Optional[str] = None
    model_config = ConfigDict(populate_by_name=True)


class TicketVisitSummaryResponse(BaseModel):
    ticket_id: int
    items: List[TicketVisitSummaryItem]


class LastVisitProductNextQty(BaseModel):
    product_id: int
    next_qty: Optional[int] = Field(default=None, ge=0, alias="nextQty", serialization_alias="nextQty")
    model_config = ConfigDict(populate_by_name=True)


class LastVisitNextQtyResponse(BaseModel):
    cost_center_id: int
    visit_id: Optional[int] = None
    visited_at: Optional[str] = None
    products: List[LastVisitProductNextQty]


class ReservationTicketItem(BaseModel):
    ticket_id: int
    cost_center_id: int
    quantity: int


class ReservationItem(BaseModel):
    product_id: int
    reserved_qty: int
    tickets: List[ReservationTicketItem]


class ReservationsResponse(BaseModel):
    generated_at: datetime
    items: List[ReservationItem]
