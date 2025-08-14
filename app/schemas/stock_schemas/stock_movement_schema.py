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
    
class ClientSalesAnchoredDTO(BaseModel):
    ticket_id: int                       # só para descobrir o start_date
    cost_center_id: int
    product_id: int
    total_sold: Optional[int] = Field(default=None, ge=0)
    per_day: Optional[Dict[date, int]] = None  # {2025-08-12: 3, ...}
    registration_dt: Optional[datetime] = None # se None, usa agora()
    distribute: Literal["even","front","back"] = "even"
    allow_negative_client_stock: bool = False