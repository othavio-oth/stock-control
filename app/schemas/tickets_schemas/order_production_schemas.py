from pydantic import BaseModel
from typing import Optional
from datetime import date

class OrderProductionBase(BaseModel):
    init: Optional[date] = None
    end: Optional[date] = None
    status: str
    production_id: int
    sale: Optional[float] = None
    cost: Optional[float] = None
    gain: Optional[float] = None
    cost_center_id: Optional[int] = None
    stock_location_id: Optional[int] = None

    class Config:
        from_attributes = True

class OrderProductionResponse(OrderProductionBase):
    id: int
    
class OrderProductionCreate(OrderProductionBase):
    init: Optional[date] = None
    end: Optional[date] = None
    status: str
    production_id: int
    sale: Optional[float] = None
    cost: Optional[float] = None
    gain: Optional[float] = None
    cost_center_id: Optional[int] = None
    stock_location_id: Optional[int] = None

class OrderProductionUpdate(OrderProductionCreate):
    pass

class OrderProductsBase(BaseModel):
    ordem_p: int
    op: int
    descrip_op: str
    id_product: int
    description_product: str
    cost_pro: float
    qtd_association: float
    qtd_total: float
    id_origin: int
    origin_name: str
    origin_product: str
    
class OrderProductsSimplified(BaseModel):
    id: int
    description: str
    qtd: float

class OrderProductsFinancial(BaseModel):
    id: int
    description: str
    cost_pro: float
    qtd: float
    cost_total: float