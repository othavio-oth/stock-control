from enum import Enum
from typing import List
from sqlalchemy import Column, DateTime, Integer, String, Boolean, Float, ForeignKey, Date, Numeric, func
from app.database.base import Base
from sqlalchemy.orm import relationship


class CostCenter(Base):
    __tablename__ = "cost_centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default=True)
    is_active = Column(Boolean, default=True, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    sellers = relationship("Seller", back_populates="cost_center", lazy='select') 
    stock_movements = relationship("StockMovement", back_populates="cost_center")




class TicketProduct(Base):
    __tablename__ = "ticket_products"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_ordered = Column(Integer, nullable=False)
    quantity_sold = Column(Integer, default=0)
    unit_price = Column(Numeric(10, 2))
    sold_until = Column(Date)
    ticket = relationship("Ticket", back_populates="products")
    product = relationship("Product")
    
    @property
    def description(self):
        return self.product.description if self.product else None


    class Config:
        from_attributes = True


class Ticket(Base):
    __tablename__ = "tickets"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    order_date = Column(Date, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    products = relationship("TicketProduct", back_populates="ticket")

    
    class Config:
        from_attributes = True

    