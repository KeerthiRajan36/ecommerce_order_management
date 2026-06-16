from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.schemas.order_item import OrderItemCreate, OrderItemResponse
from app.schemas.customer import CustomerResponse
import enum


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class OrderBase(BaseModel):
    customer_id: int


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None


class OrderResponse(OrderBase):
    id: int
    total_amount: float
    status: OrderStatus
    order_date: datetime
    created_at: datetime
    updated_at: Optional[datetime]
    items: List[OrderItemResponse] = []
    customer: Optional[CustomerResponse] = None
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    total_records: int
    current_page: int
    limit: int
    data: List[OrderResponse]