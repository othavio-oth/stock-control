from pydantic import BaseModel
from typing import List, Optional

from app.schemas.products_schemas.products_schemas import ProductResponse

class Category(BaseModel):
    name: str
    description: Optional[str] = None
    status: bool = True

class CategoryCreate(Category):
    pass

class CategoryUpdate(Category):
    pass

class CategoryResponse(Category):
    id: int
    products: List[ProductResponse] 