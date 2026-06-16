from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.database import Base

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer,primary_key=True,index=True)
    customer_id = Column(Integer,ForeignKey("customers.id"),nullable=False)
    total_amount = Column(Float,nullable=False,default=0.0)
    status = Column(Enum(OrderStatus),default=OrderStatus.PENDING)
    order_date = Column(DateTime(timezone=True),server_default=func.now())
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())

    customer = relationship("Customer",back_populates="orders")
    items = relationship("OrderItem",back_populates="order",cascade="all,delete-orphan")
    shipment = relationship("Shipment",back_populates="order",uselist=False,cascade="all, delete-orphan")
    