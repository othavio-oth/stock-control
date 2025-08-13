from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date


class TicketProductBase(BaseModel):
    ticket_id: Optional[int] = None
    product_id: int
    quantity_ordered: float
    unit_price: Optional[float] = None
    entry_price: Optional[float] = None

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

        
class TicketProductUpdate(TicketProductBase):
    id: int


class TicketProductCreate(TicketProductBase):
    pass


class TicketProductResponse(TicketProductBase):
    id: int
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)




class TicketBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str
    order_date: Optional[date] = None
    cost_center_id: int
    created_by: int

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)



class TicketCreate(TicketBase):
    products: List[TicketProductCreate] = []



class TicketUpdate(TicketBase):
    pass


class TicketRegisterSales(TicketBase):
    id: int
    products: List[TicketProductBase] = []

class TicketResponse(TicketBase):
    id: int
    products: List[TicketProductResponse] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class TicketSalesResponse(BaseModel):
    message: str
    ticket_id: int
    total_products: int