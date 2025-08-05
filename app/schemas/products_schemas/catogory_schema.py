from pydantic import BaseModel
from typing import Optional

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