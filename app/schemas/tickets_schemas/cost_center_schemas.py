from pydantic import BaseModel
from typing import Optional

from app.schemas.products_schemas.commom_schemas import RetailChainResponseWithoutCostCenters


class CostCenterBase(BaseModel):
    name: str
    description: Optional[str] = None


class CostCenterCreate(CostCenterBase):
    retail_chain_id: int

    pass

class CostCenterUpdate(CostCenterBase):
    retail_chain_id: int
    pass

class CostCenterResponse(CostCenterBase):
    id: int
    retail_chain:RetailChainResponseWithoutCostCenters
    
    class Config:
        from_attributes = True