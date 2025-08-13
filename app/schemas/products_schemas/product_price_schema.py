from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal

class ProductPriceHistoryBase(BaseModel):
    product_id: int
    price: Annotated[Decimal, Field(max_digits=10, decimal_places=2)]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ProductPriceHistoryCreate(ProductPriceHistoryBase):
    retail_chain_id: Optional[int] = None
    cost_center_id: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "product_id": 1,
                "price": Decimal("99.90"),
                "retail_chain_id": 1,
                "cost_center_id": None,
                "start_date": "2023-01-01T00:00:00"
            }
        }
    )

class ProductPriceHistoryUpdate(BaseModel):
    price: Optional[Annotated[Decimal, Field(max_digits=10, decimal_places=2)]] = None

class RetailChainSimple(BaseModel):
    id: int
    name: str

class CostCenterSimple(BaseModel):
    id: int
    name: str

class ProductSimple(BaseModel):
    id: int
    name: str

class ProductPriceHistoryResponse(ProductPriceHistoryBase):
    id: int
    retail_chain: Optional[RetailChainSimple] = None
    cost_center: Optional[CostCenterSimple] = None
    product: ProductSimple

    model_config = ConfigDict(from_attributes=True) 
    
    
class ProductCurrentPriceResponse(BaseModel):
    product_id: int
    price: Optional[float] = None
    source: Optional[str] = None  # "cost_center" | "retail_chain" | "default" | None

    model_config = ConfigDict(from_attributes=True)
    
class UnitPricePayload(BaseModel):
    unit_price: float
