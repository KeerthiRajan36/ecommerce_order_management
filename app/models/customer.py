from sqlalchemy import Column,Integer,String,DateTime,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String(100),nullable=False)
    email = Column(String(100),unique=True,nullable=False,index=True)
    phone = Column(String(20),nullable=False)
    address = Column(String(255),nullable=False)
    is_active = Column (Boolean,default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())

    orders = relationship("Order",back_populates="customer",
                          cascade="all,delete-orphan")