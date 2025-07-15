from pydantic import BaseModel
from typing import Optional
from typing import List

from app.schemas.users_schemas.seller_schema import  SellerWithUser

class CostCenterBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[bool] = True

class CostCenterCreate(CostCenterBase):
    pass

class CostCenterUpdate(CostCenterBase):
    pass

class CostCenterResponse(CostCenterBase):
    id: int
    sellers: List[SellerWithUser] = []  
    
    class Config:
        from_attributes = True