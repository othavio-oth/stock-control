from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.stockMovement import MovementType


class StockMovementBase(BaseModel):
    product_id: int
    quantity: int

    
class StockMovementLost(StockMovementBase):
    cost_center_id: Optional[int] = None
    movement_type: str = MovementType.LOST.value  # Valor fixo para perdas
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permite conversão de/para ORM
        


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
    supplier: Optional[str] = None

    class Config:
        from_attributes = True 
        
class StockTotal(BaseModel):
    product_id: int
    total: int
    

class TotalProductStockResponse(StockTotal):
    pass
    