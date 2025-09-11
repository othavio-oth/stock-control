from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class ProductCostHistoryRead(BaseModel):
    id: int
    product_id: int
    cost: float
    start_date: datetime
    end_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

