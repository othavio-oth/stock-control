from sqlalchemy import CheckConstraint, Column, DateTime, Index, Integer, String, Boolean, Float, ForeignKey, Date, Numeric, UniqueConstraint, func, select
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
    price_history = relationship("ProductPriceHistory", back_populates="retail_chain",
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
    start_date = Column(DateTime, nullable=False, server_default=func.now())
    end_date = Column(DateTime, nullable=True, index=True)  # NULL = vigente

    product = relationship("Product", back_populates="cost_history")


class ProductPriceHistory(Base):
    __tablename__ = "product_price_history"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Hierarquia de preços (apenas UM pode ser preenchido):
    retail_chain_id = Column(Integer, ForeignKey("retail_chains.id"), nullable=True)  # Preço para toda a rede
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True)    # Preço específico para 1 cliente
    
    retail_chain = relationship("RetailChain")
    price = Column(Numeric(10, 2), nullable=False)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=True)  # NULL = preço atual

    # Validação: só permite vincular a rede OU cliente, não ambos
    __table_args__ = (
        CheckConstraint(
            '(retail_chain_id IS NOT NULL AND cost_center_id IS NULL) OR (retail_chain_id IS NULL AND cost_center_id IS NOT NULL)',
            name='check_price_hierarchy'
        ),
        UniqueConstraint('product_id', 'retail_chain_id', 'start_date', name='uix_product_chain_start'),
        UniqueConstraint('product_id', 'cost_center_id', 'start_date', name='uix_product_cost_center_start')
    )

    # Relacionamentos
    product = relationship("Product", back_populates="price_history")
    retail_chain = relationship("RetailChain")
    cost_center = relationship("CostCenter")


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    contact_email = Column(String(150), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    address = Column(String(250), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relacionamento com StockMovement, para saber de qual fornecedor veio a entrada
    stock_movements = relationship("StockMovement", back_populates="supplier")
    