from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Date, Numeric
from app.database.base import Base
from app.models.groups import Product

class CostCenter(Base):
    __tablename__ = "cost_centers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True)

class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, default=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    init = Column(Date, nullable=True)
    end = Column(Date, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

class TicketProduct(Base):
    __tablename__ = "ticket_products"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("ticket.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    correction_factor = Column(Float, nullable=False)

class StockProducts(Base):
    __tablename__ = "stock_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    owner = Column(Integer, ForeignKey("users.id"), nullable=False)

class StockProductsHistory(Base):
    __tablename__ = "stock_products_history"

    id = Column(Integer, primary_key=True, index=True)
    stock_product_id = Column(Integer, ForeignKey("stock_products.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("ticket.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    date = Column(Date, nullable=False)
