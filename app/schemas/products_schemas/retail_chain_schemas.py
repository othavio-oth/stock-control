from pydantic import BaseModel
from typing import List, Optional

from app.schemas.products_schemas.commom_schemas import RetailChainBase, RetailChainResponseWithoutCostCenters
from app.schemas.tickets_schemas.cost_center_schemas import CostCenterResponse


class RetailChainCreate(RetailChainBase):
    pass

class RetailChainUpdate(RetailChainBase):
    id: int
    pass

class RetailChainResponse(RetailChainResponseWithoutCostCenters ):
    cost_centers:List[CostCenterResponse]
    
class RetailChainResponseWithoutCostCenters(RetailChainBase):
    id: int
    
    class Config:
        from_attributes = True