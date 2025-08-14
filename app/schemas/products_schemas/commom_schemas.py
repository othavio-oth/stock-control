from pydantic import BaseModel

class RetailChainBase(BaseModel):
    name: str
    description: str | None = None

class RetailChainResponseWithoutCostCenters(RetailChainBase):
    id: int
    
    class Config:
        from_attributes = True