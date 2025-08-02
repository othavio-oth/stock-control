from sqlalchemy import Column, DateTime, Integer, String, Boolean, Float, ForeignKey, Date, Numeric
from sqlalchemy.orm import relationship
from app.database.base import Base

class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(Boolean, default=True)
    
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
    
class TypeRegistration(Base):
    __tablename__ = "type_registration"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), unique=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Boolean, default=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    custom_id = Column(Integer, unique=True, nullable=True)
    description = Column(String, nullable=False)
    status = Column(Boolean, default=True)
    type_registration_id = Column(Integer, ForeignKey("type_registration.id"), nullable=True)
    group_id = Column(Integer, ForeignKey("group.id"), nullable=True)
    cost_inside = Column(Float, nullable=False)
    conversion_id = Column(Integer, ForeignKey("unit_conversion.id"), nullable=True)
    cost_output = Column(Float, nullable=False)
    un_inside_id = Column(Integer, ForeignKey("unit_measurement.id"), nullable=False)
    un_output_stock_id = Column(Integer, ForeignKey("unit_measurement.id"), nullable=False)
    cost_taxation_id = Column(Integer, ForeignKey("cost_taxation.id"), nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)  # Campo de status
    deleted_at = Column(DateTime, nullable=True)
    
    stock_movements = relationship("StockMovement", back_populates="product")


    cost_taxation = relationship("CostTaxation", back_populates="products")

class CostTaxation(Base):
    __tablename__ = "cost_taxation"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    taxation = Column(Numeric(15, 4), nullable=False)
    logistic = Column(Numeric(15, 4), nullable=False)
    mld_taxation = Column(Numeric(15, 4), nullable=False)
    prejudice = Column(Numeric(15, 4), nullable=False)

    products = relationship("Product", back_populates="cost_taxation", cascade="all, delete-orphan")