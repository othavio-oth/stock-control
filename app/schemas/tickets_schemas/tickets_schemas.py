from pydantic import BaseModel
from typing import Optional
from datetime import date

class TicketBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str
    order_date: Optional[date] = None
    cost_center_id: int
    created_by: int

    class Config:
        from_attributes = True

class TicketCreate(TicketBase):
    name: str
    description: Optional[str] = None
    status: str
    order_date: Optional[date] = None
    cost_center_id: int

class TicketUpdate(TicketBase):
    pass

class TicketResponse(TicketBase):
    id: int
    
class TicketProductList(TicketResponse):
    product_ids: list[int]

class TicketProductBase(BaseModel):
    ticket_id: int
    product_id: int
    quantity_ordered: float
    quantity_sold: Optional[float] = 0
    sold_until: Optional[date] = None
    # correction_factor: float

class TicketProductCreate(TicketProductBase):
    pass

class TicketProductResponse(TicketProductBase):
    id: int