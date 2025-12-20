from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base

class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    cost_center_id = Column(Integer, ForeignKey("cost_centers.id"), nullable=False)

    user = relationship("User", back_populates="seller_profile")
    cost_center = relationship("CostCenter", back_populates="sellers")

    def __repr__(self):
        return f"<Seller(user_id={self.user_id}, cost_center_id={self.cost_center_id})>"
