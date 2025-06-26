from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductionBase(BaseModel):
    description: str
    
class ProductionCreate(ProductionBase):
    id: int

class ProductionResponse(ProductionCreate):
    pass
    
class ProductionFabricationCreate(BaseModel):
    fabrication_id: int
    production_id: int
    quantity: float

class ProductionFabricationList(BaseModel):
    id: int
    fabrication_id: int
    production_id: int
    quantity: float
    description: str

class ProductionFabricationDelete(ProductionFabricationList):
    pass