from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProductBase(BaseModel):
    custom_id: Optional[int] = None
    name: str
    category_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    is_active: Optional[bool] = True
    deleted_at: Optional[date] = None
    current_cost: Optional[float] = None
    default_price: Optional[float] = None
    
    class Config:
        from_attributes = True  
    
    
class ProductEntryHistoryResponse(BaseModel):
    id: int
    description: str
    custom_id: int
    
class ProductsPageResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    

    