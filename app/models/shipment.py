from sqlalchemy import Column, Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base


class ShipmentStatus(str, enum.Enum):
    PENDING = "pending"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class Shipment(Base):
    __tablename__ = "shipments"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    tracking_number = Column(String(100), unique=True, nullable=False)
    status = Column(Enum(ShipmentStatus), default=ShipmentStatus.PENDING)
    shipped_date = Column(DateTime(timezone=True), nullable=True)
    delivered_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
    order = relationship("Order", back_populates="shipment")