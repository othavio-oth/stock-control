from pydantic import BaseModel
from typing import List, Optional

from app.schemas.tickets_schemas.cost_center_schemas import CostCenterResponse

class RetailChainBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: bool = True

class RetailChainCreate(RetailChainBase):
    pass

class RetailChainUpdate(RetailChainBase):
    pass

class RetailChainResponse(RetailChainBase):
    id: int
    cost_centers:List[CostCenterResponse]