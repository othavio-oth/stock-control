from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductBase(BaseModel):
    custom_id: Optional[int] = None
    description: str
    status: bool = True
    type_registration_id: int
    group_id: int
    date_cost: date
    cost_inside: float
    conversion_id: Optional[int] = None
    cost_output: float
    un_inside_id: int
    un_output_stock_id: int
    cost_taxation_id: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int