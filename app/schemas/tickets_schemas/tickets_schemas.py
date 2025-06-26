from pydantic import BaseModel
from typing import Optional
from datetime import date

class TicketBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str
    init: Optional[date] = None
    end: Optional[date] = None
    cost_center_id: int
    created_by: int

    class Config:
        from_attributes = True

class TicketCreate(TicketBase):
    name: str
    description: Optional[str] = None
    status: str
    init: Optional[date] = None
    end: Optional[date] = None
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
    quantity: float
    correction_factor: float

class TicketProductCreate(TicketProductBase):
    pass

class TicketProductResponse(TicketProductBase):
    id: int