from typing import List
from pydantic import BaseModel

from app.schemas.products_schemas.products_schemas import ProductResponse
from app.schemas.tickets_schemas.cost_center_schemas import CostCenterResponse
from app.schemas.tickets_schemas.tickets_schemas import TicketResponse


class ListAllResponse(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int

class AllProductsResponse(ListAllResponse):
    items: List[ProductResponse]
    
class AllCostCentersResponse(ListAllResponse):
    items: List[CostCenterResponse]

class AllTicketsResponse(ListAllResponse):
    items: List[TicketResponse]
