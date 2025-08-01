from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database.base import Base

class MovementType(str, enum.Enum):
    SYSTEM_IN = "system_in"             # entrada no sistema
    TO_COST_CENTER = "to_cost_center"   # enviado para um cliente/cost center
    SOLD = "sold"                        # vendido pelo cliente
    LOST = "lost"                        # perda

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(Enum(MovementType), nullable=False)
    supplier = Column(String, nullable=True)  
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True) 

    product = relationship("Product", back_populates="stock_movements")
    cost_center = relationship("CostCenter", back_populates="stock_movements")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
