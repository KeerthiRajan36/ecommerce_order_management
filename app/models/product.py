from sqlalchemy import Column,String,Integer,Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(200),nullable=False)
    description = Column(String(1000),nullable=True)
    price = Column(Float,nullable=True)
    stock_quantity = Column(Integer,nullable=True,default=0)
    category = Column(String(100),nullable=True)
    is_active = Column(Boolean,default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())

    order_items = relationship("OrderItem",back_populates="product")
    