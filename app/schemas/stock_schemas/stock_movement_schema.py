from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, Literal, Optional, List
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
        
class StockEntryRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_cost: Optional[float] = None
    supplier_id: Optional[int] = None
    supplier_name: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SupplierPurchaseUpdateDTO(BaseModel):
    quantity: Optional[int] = None
    unit_cost: Optional[float] = None
    supplier_id: Optional[int] = None

    def ensure_not_empty(self):
        if self.quantity is None and self.unit_cost is None and self.supplier_id is None:
            raise ValueError("Nenhum campo para atualizar.")

class StockEntryReadWithCost(StockEntryRead):
    current_avg_cost: Optional[float] = None


class SupplierPurchaseBulkDTO(BaseModel):
    items: List[SupplierPurchaseDTO]

    model_config = ConfigDict(from_attributes=True)

class StockTotal(BaseModel):
    product_id: int
    total: int
    
class InventoryResponse(StockMovementBase):
    id: int
    

class TotalProductStockResponse(StockTotal):
    pass
    

class ClientStockUpdateRequest(BaseModel):
    cost_center_id: int = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    upsert: bool = True  # opcional; default True
    
class ClientStockResponse(BaseModel):
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)
    
class RegisterClientSalesDTO(BaseModel):
    cost_center_id: int
    product_id: int
    total_sold: int = Field(gt=0)           # > 0
    registration_date: date  


class ClientSalesHistoryRead(BaseModel):
    id: int
    cost_center_id: int
    product_id: int
    date: date
    sold_quantity: int

    model_config = ConfigDict(from_attributes=True)


class ClientLossHistoryRead(BaseModel):
    id: int
    cost_center_id: int
    product_id: int
    date: date
    lost_quantity: int
    reason: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ClientSalesLossHistoryRead(BaseModel):
    cost_center_id: int
    product_id: int
    date: date
    sold_quantity: int = 0
    lost_quantity: int = 0
    previous_ticket_id: Optional[int] = None
    previous_ticket_order_date: Optional[date] = None
    previous_ticket_name: Optional[str] = None
    previous_ticket_quantity: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class SalesQuantityResponse(BaseModel):
    product_id: int
    start_date: date
    end_date: date
    total_sold: int
    cost_center_id: Optional[int] = None
    retail_chain_id: Optional[int] = None


class ClientSalesUpdateDTO(BaseModel):
    cost_center_id: int
    product_id: int
    date: date
    total_sold: int = Field(ge=0)


class ClientSalesUpdateResult(BaseModel):
    cost_center_id: int
    product_id: int
    date: date
    total_sold: int
