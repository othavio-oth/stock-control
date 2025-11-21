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
    sellers = relationship("Seller", back_populates="cost_center", lazy='select', cascade="all, delete-orphan") 
    stock_movements = relationship("StockMovement", back_populates="cost_center", cascade="all, delete-orphan")
    retail_chain_id = Column(Integer, ForeignKey("retail_chains.id"), nullable=True)

    is_active = Column(Boolean, default=True, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    retail_chain = relationship("RetailChain", back_populates="cost_centers")





class TicketProduct(Base):
    __tablename__ = "ticket_products"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_ordered = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2))
    entry_price = Column(Numeric(10, 2))
    ticket = relationship("Ticket", back_populates="products")
    product = relationship("Product")

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
    approved_at = Column(DateTime, nullable=True)
    sales_start_date = Column(Date, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    products = relationship("TicketProduct", back_populates="ticket",     cascade="all, delete-orphan"
)
    inventory_visits = relationship("InventoryVisit", back_populates="ticket", cascade="all, delete-orphan")


    class Config:
        from_attributes = True

    
