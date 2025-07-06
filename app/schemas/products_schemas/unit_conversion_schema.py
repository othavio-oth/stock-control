from pydantic import BaseModel
from typing import Optional

class ConversionBase(BaseModel):
    unit_from: int
    unit_to: int
    conversion: float
    status: bool = True

class ConversionCreate(ConversionBase):
    pass

class ConversionUpdate(ConversionBase):
    pass

class ConversionResponse(ConversionBase):
    id: int