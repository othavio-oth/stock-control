from pydantic import BaseModel
from typing import Optional

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