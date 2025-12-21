from typing import List
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class ProductSalesAnalyticsResponse(BaseModel):
    product_id: int
    product_name: str
    cost_center_id: int
    cost_center_name: str
    period_days: int
    
    # Métricas Essenciais
    total_sold: int
    total_revenue: Decimal
    avg_sale_price: Decimal
    stock_utilization: float  # % do estoque que foi vendido
    
    # Lucratividade
    total_profit: Decimal
    profit_margin: float      # Em porcentagem
    
    # Perdas
    total_losses: int
    loss_percentage: float    # Em porcentagem
    


class CycleAnalysis(BaseModel):
    ticket_id: int
    start: str
    end: str
    period_hours: float
    sent_qty_prev_cycle: int
    current_client_stock: int
    losses_in_period: int
    inferred_sold_qty: int
    avg_per_hour: float
    avg_per_day: float
    status: str

class ProductHistoryAnalysis(BaseModel):
    product_id: int
    cycles: List[CycleAnalysis]

class MultiCycleAnalysisResponse(BaseModel):
    ticket_id: int
    max_cycles: int
    items: List[ProductHistoryAnalysis]
    model_config = ConfigDict(from_attributes=True)
