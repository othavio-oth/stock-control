from sqlalchemy import Column, DateTime, Index, Integer, String, Boolean, Float, ForeignKey, Date, Numeric, UniqueConstraint, func, select
from sqlalchemy.orm import relationship
from app.database.base import Base
from sqlalchemy.ext.hybrid import hybrid_property

class RetailChain(Base):
    __tablename__ = "retail_chains"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(Boolean, default=True)
    
    cost_centers = relationship("CostCenter", back_populates="retail_chain")
    price_history = relationship("ProductPriceHistory", back_populates="chain",
                                 order_by="ProductPriceHistory.start_date.desc()",
                                 cascade="all, delete-orphan")

    
class UnitMeasurement(Base):
    __tablename__ = "unit_measurement"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    
class UnitConversion(Base):
    __tablename__ = "unit_conversion"

    id = Column(Integer, primary_key=True, index=True)
    unit_from = Column(Integer, ForeignKey("unit_measurement.id"), nullable=False)
    unit_to = Column(Integer, ForeignKey("unit_measurement.id"), nullable=False)
    conversion = Column(Float, nullable=False)
    status = Column(Boolean, default=True)
    
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True)
    
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    custom_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)  # Campo de status
    deleted_at = Column(DateTime, nullable=True)
    
    category = relationship("Category", back_populates="products")
    stock_movements = relationship("StockMovement", back_populates="product")
    cost_history = relationship("ProductCostHistory", back_populates="product",
                                order_by="ProductCostHistory.start_date.desc()",
                                cascade="all, delete-orphan")
    price_history = relationship("ProductPriceHistory", back_populates="product",
                                 order_by="ProductPriceHistory.start_date.desc()",
                                 cascade="all, delete-orphan")
    @hybrid_property
    def current_cost(self):
        
        active = next((c for c in self.cost_history if c.end_date is None), None)
        return active.cost if active else None
    
    @hybrid_property
    def default_price(self):
        """Preço padrão quando não associado a uma retail chain"""
        default = next((p for p in self.price_history 
                       if p.retail_chain_id is None and p.end_date is None), None)
        return default.price if default else None
    
class ProductCostHistory(Base):
    __tablename__ = "product_cost_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    cost = Column(Numeric(10, 2), nullable=False)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)

    start_date = Column(DateTime, nullable=False, server_default=func.now())
    end_date = Column(DateTime, nullable=True, index=True)  # NULL = vigente

    product = relationship("Product", back_populates="cost_history")
    cost_center = relationship("CostCenter")


class ProductPriceHistory(Base):
    __tablename__ = "product_price_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    chain_id = Column(Integer, ForeignKey("retail_chains.id"), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    start_date = Column(DateTime, nullable=False, server_default=func.now())
    end_date = Column(DateTime, nullable=True, index=True)  # NULL = vigente

    product = relationship("Product", back_populates="price_history")
    chain = relationship("RetailChain", back_populates="price_history")

    __table_args__ = (
        # evita inserções duplicadas idênticas; a unicidade do "vigente" é garantida pela lógica de app
        UniqueConstraint("product_id", "chain_id", "start_date", name="uix_product_chain_start"),
        Index("ix_product_chain_active", "product_id", "chain_id", "end_date")
    )


