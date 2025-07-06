from pydantic import BaseModel
from typing import Optional

class StockLocationBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: bool = True

class StockLocationResponse(StockLocationBase):
    id: int