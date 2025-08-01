from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class StockMovementBase(BaseModel):
    product_id: int
    quantity: int
    # movement_type: MovementType
    # source_cost_center_id: Optional[int] = None
    # destination_cost_center_id: Optional[int] = None

class StockMovementSaleCreate(StockMovementBase):
    product_id: int
    quantity: int
    cost_center_id: Optional[int] = None
    
class SystemInStockMovement(StockMovementBase):
    supplier: str

class StockMovementRead(StockMovementBase):
    id: int
    created_at: datetime
    cost_center_id: Optional[int] = None
    movement_type: str

    class Config:
        from_attributes = True 
        
class StockTotal(BaseModel):
    product_id: int
    total: int
    

class TotalProductStockResponse(StockTotal):
    pass
    