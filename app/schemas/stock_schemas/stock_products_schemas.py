from pydantic import BaseModel
from datetime import date

class StockProductBase(BaseModel):
    name: str
    owner: int

class StockProductCreate(StockProductBase):
    pass

class StockProductUpdate(StockProductBase):
    pass

class StockProductResponse(StockProductBase):
    id: int

class StockProductHistoryBase(BaseModel):
    stock_product_id: int
    ticket_id: int
    quantity: float
    cost_center_id: int
    date: date

class StockProductHistoryCreate(StockProductHistoryBase):
    pass

class StockProductHistoryUpdate(StockProductHistoryBase):
    pass

class StockProductHistoryResponse(StockProductHistoryBase):
    id: int
