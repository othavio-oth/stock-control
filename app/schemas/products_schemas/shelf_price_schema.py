from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.products_schemas.product_price_schema import (
    CostCenterSimple,
    ProductSimple,
    RetailChainSimple,
)


class ShelfPriceBase(BaseModel):
    product_id: int
    percentage_rate: Annotated[Decimal, Field(max_digits=10, decimal_places=4)]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ShelfPriceCreate(ShelfPriceBase):
    retail_chain_id: Optional[int] = None
    cost_center_id: Optional[int] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "product_id": 1,
                "percentage_rate": Decimal("15.2500"),
                "retail_chain_id": 1,
                "cost_center_id": None,
                "start_date": "2025-01-01T00:00:00",
            }
        }
    )


class ShelfPriceUpdate(BaseModel):
    percentage_rate: Optional[Annotated[Decimal, Field(max_digits=10, decimal_places=4)]] = None
    retail_chain_id: Optional[int] = None
    cost_center_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ShelfPriceResponse(ShelfPriceBase):
    id: int
    retail_chain: Optional[RetailChainSimple] = None
    cost_center: Optional[CostCenterSimple] = None
    product: ProductSimple

    model_config = ConfigDict(from_attributes=True)
