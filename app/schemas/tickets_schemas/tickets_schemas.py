from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class TicketProductBase(BaseModel):
    ticket_id: int
    product_id: int
    quantity_ordered: float
    quantity_sold: Optional[float] = 0
    sold_until: Optional[date] = None
    unit_price: Optional[float] = None
    entry_price: Optional[float] = None

    class Config:
        from_attributes = True
        
class TicketProductUpdate(TicketProductBase):
    id: int


class TicketProductCreate(TicketProductBase):
    pass


class TicketProductResponse(TicketProductBase):
    id: int
    description: Optional[str] = None


    class Config:
        from_attributes = True



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
    pass


class TicketUpdate(TicketBase):
    pass


class TicketRegisterSales(TicketBase):
    id: int
    products: List[TicketProductBase] = []

class TicketResponse(TicketBase):
    id: int
    products: List[TicketProductResponse] = []

    class Config:
        from_attributes = True

class TicketSalesResponse(BaseModel):
    message: str
    ticket_id: int
    total_products: int