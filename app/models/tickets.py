from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Date, Numeric
from app.database.base import Base
from sqlalchemy.orm import relationship


class CostCenter(Base):
    __tablename__ = "cost_centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default=True)
    
    sellers = relationship("Seller", back_populates="cost_center", lazy='select') 




class Ticket(Base):
    __tablename__ = "tickets"


    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    order_date = Column(Date, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

class TicketProduct(Base):
    __tablename__ = "ticket_products"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity_ordered = Column(Integer, nullable=False)
    quantity_sold = Column(Integer, default=0)
    sold_until = Column(Date)

    
    # correction_factor = Column(Float, nullable=False)

class StockProducts(Base):
    __tablename__ = "stock_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    owner = Column(Integer, ForeignKey("users.id"), nullable=False)

class StockProductsHistory(Base):
    __tablename__ = "stock_products_history"

    id = Column(Integer, primary_key=True, index=True)
    stock_product_id = Column(Integer, ForeignKey("stock_products.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    date = Column(Date, nullable=False)
