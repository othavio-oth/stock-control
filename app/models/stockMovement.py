from sqlalchemy import Column, Date, Integer, Numeric, String, Enum, ForeignKey, DateTime, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from sqlalchemy import Enum as SAEnum

from app.database.base import Base

class MovementType(enum.Enum):
    SUPPLIER_PURCHASE = "supplier_purchase"  # Entrada no estoque (compra do produtor)
    TO_CLIENT = "to_client"                  # Saída do seu estoque para cliente
    CLIENT_SALE = "client_sale"               # Venda do cliente para consumidor final
    CLIENT_LOSS = "client_loss"               # Perda no cliente
    SUPPLIER_LOSS = "supplier_loss"           # Perda no seu próprio estoque


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(
    SAEnum(
        MovementType,
        name="movement_type",  # nome do tipo ENUM no Postgres
        values_callable=lambda enum_cls: [e.value for e in enum_cls],
        native_enum=True,
        validate_strings=True,
    ),
    nullable=False,
)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=True) 
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=True) 
    product_unit_cost = Column(Numeric(10, 2), nullable=True)
    inventory_visit_id = Column(Integer, ForeignKey("inventory_visits.id", ondelete="SET NULL"), nullable=True)


    product = relationship("Product", back_populates="stock_movements")
    cost_center = relationship("CostCenter", back_populates="stock_movements")
    supplier = relationship("Supplier")
    inventory_visit = relationship("InventoryVisit", back_populates="movements")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ClientStock(Base):
    __tablename__ = "client_stock"

    id = Column(Integer, primary_key=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    last_observed_at = Column(DateTime(timezone=True), nullable=True)
    last_zeroed_at = Column(DateTime(timezone=True), nullable=True)

    product = relationship("Product")
    cost_center = relationship("CostCenter")
    
class ClientSalesHistory(Base):
    __tablename__ = "client_sales_history"

    id = Column(Integer, primary_key=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    date = Column(Date, nullable=False)
    sold_quantity = Column(Integer, nullable=False)
    observed_at = Column(DateTime(timezone=True), nullable=True)

    product = relationship("Product")
    cost_center = relationship("CostCenter")
    __table_args__ = (
        UniqueConstraint("cost_center_id", "product_id", "date", name="uq_sales_day"),
    )

class ReplenishmentRecommendation(Base):
    __tablename__ = "replenishment_recommendations"

    id = Column(Integer, primary_key=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    recommendation_date = Column(DateTime, default=func.now())
    recommendation = Column(String, nullable=False)  # "Enviar mais", "Estoque OK"
    reason = Column(String, nullable=True)

    product = relationship("Product")
    cost_center = relationship("CostCenter")
    


class InventoryStock(Base):
    __tablename__ = "inventory_stock"

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

    product = relationship("Product")

class ClientLossHistory(Base):
    __tablename__ = "client_loss_history"

    id = Column(Integer, primary_key=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    date = Column(Date, nullable=False)
    lost_quantity = Column(Integer, nullable=False)
    reason = Column(String, nullable=True)
    observed_at = Column(DateTime(timezone=True), nullable=True)

    product = relationship("Product")
    cost_center = relationship("CostCenter")


class InventoryVisit(Base):
    __tablename__ = "inventory_visits"

    id = Column(Integer, primary_key=True)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    recorded_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    visited_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    total_stock_quantity = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)

    cost_center = relationship("CostCenter")
    ticket = relationship("Ticket", back_populates="inventory_visits")
    recorded_user = relationship("User")
    movements = relationship("StockMovement", back_populates="inventory_visit")
    products = relationship(
        "InventoryVisitProduct",
        back_populates="visit",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class InventoryVisitProduct(Base):
    __tablename__ = "inventory_visit_products"

    id = Column(Integer, primary_key=True)
    inventory_visit_id = Column(
        Integer,
        ForeignKey("inventory_visits.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    sales_quantity = Column(Integer, nullable=False, default=0)
    loss_quantity = Column(Integer, nullable=False, default=0)
    next_quantity = Column(Integer, nullable=True)

    visit = relationship("InventoryVisit", back_populates="products")
    product = relationship("Product")

    @property
    def next_qty(self):
        return self.next_quantity

    @next_qty.setter
    def next_qty(self, value):
        self.next_quantity = value
