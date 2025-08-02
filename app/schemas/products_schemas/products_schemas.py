from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProductBase(BaseModel):
    custom_id: Optional[int] = None
    description: str
    status: bool = True
    type_registration_id: Optional[int] = None
    group_id: Optional[int] = None
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
    is_active: Optional[bool] = True
    
class ProductsPageResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int