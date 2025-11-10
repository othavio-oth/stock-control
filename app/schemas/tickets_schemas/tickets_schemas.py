from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, List, Optional
from datetime import date

from app.schemas.tickets_schemas.inventory_visit_schema import InventoryVisitResponse

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


class TicketProductUpdateDTO(BaseModel):
    quantity_ordered: Optional[Annotated[int, Field(strict=True, ge=0)]] = None
    unit_price: Optional[Annotated[float, Field(max_digits=10, decimal_places=2)]] = None
    entry_price: Optional[Annotated[float, Field(max_digits=10, decimal_places=2)]] = None

    def ensure_not_empty(self):
        if all(v is None for v in self.model_dump().values()):
            raise ValueError("Nenhum campo para atualizar.")

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
    inventory_visits: List[InventoryVisitResponse] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

class TicketSalesResponse(BaseModel):
    message: str
    ticket_id: int
    total_products: int
