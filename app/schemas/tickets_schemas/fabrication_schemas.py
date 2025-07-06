from pydantic import BaseModel
from typing import Optional


class FabricationBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: bool = True

class FabricationCreate(FabricationBase):
    pass

class FabricationUpdate(FabricationBase):
    pass

class FabricationResponse(FabricationBase):
    id: int
    
class FabricationProductList(FabricationResponse):
    product_ids: list[int]

class FabricationProductRevenueBase(BaseModel):
    fabrication_id: int
    product_id: Optional[int] = None
    revenue_id: Optional[int] = None
    quantity: float
    correction_factor: float

class FabricationProductCreate(FabricationProductRevenueBase):
    pass

class FabricationProductResponse(FabricationProductRevenueBase):
    id: int
    
class FabricationCostsBase(FabricationBase):
    fabrication_id: int
    unit_cost: float
    cost_corrections: float
    total_cost: float

class FabricationCostsReponse(FabricationCostsBase):
    id: int