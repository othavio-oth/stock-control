from pydantic import BaseModel
from typing import Optional

class UnitMeasurementBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: bool = True

class UnitMeasurementCreate(UnitMeasurementBase):
    pass

class UnitMeasurementUpdate(UnitMeasurementBase):
    pass

class UnitMeasurementResponse(UnitMeasurementBase):
    id: int