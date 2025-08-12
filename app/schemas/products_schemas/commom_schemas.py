from pydantic import BaseModel

class RetailChainBase(BaseModel):
    name: str
    description: str | None = None
    status: bool

class RetailChainResponseWithoutCostCenters(RetailChainBase):
    id: int
    
    class Config:
        from_attributes = True