from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Literal, Optional
from datetime import date, datetime

from app.models.stockMovement import MovementType


class StockMovementBase(BaseModel):
    product_id: int
    quantity: int

    
class StockMovementLost(StockMovementBase):
    cost_center_id: Optional[int] = None
    movement_type: str = MovementType.CLIENT_LOSS.value  # Valor fixo para perdas
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permite conversão de/para ORM
        


class StockMovementSaleCreate(StockMovementBase):
    cost_center_id: Optional[int] = None
    
class SupplierPurchaseDTO(StockMovementBase):
    supplier_id: int
    unit_cost: float
    

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
    
class InventoryResponse(StockMovementBase):
    id: int
    

class TotalProductStockResponse(StockTotal):
    pass
    
class ClientStockResponse(BaseModel):
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)
    
class RegisterClientSalesDTO(BaseModel):
    cost_center_id: int
    product_id: int
    total_sold: int = Field(gt=0)           # > 0
    registration_date: date  