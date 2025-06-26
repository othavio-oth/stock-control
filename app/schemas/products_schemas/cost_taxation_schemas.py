from pydantic import BaseModel
from typing import Optional

class CostTaxationBase(BaseModel):
    description: str
    taxation: float
    logistic: float
    mld_taxation: float
    prejudice: float

class CostTaxationCreate(CostTaxationBase):
    pass

class CostTaxationUpdate(CostTaxationBase):
    pass

class CostTaxationResponse(CostTaxationBase):
    id: int