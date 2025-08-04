from pydantic import BaseModel
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