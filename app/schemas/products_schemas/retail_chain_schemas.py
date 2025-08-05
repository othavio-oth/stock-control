from pydantic import BaseModel
from typing import Optional

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