from pydantic import BaseModel, Field
from typing import Optional


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderItemCreate(OrderItemBase):
    price: float = Field(..., gt=0)


class OrderItemResponse(OrderItemBase):
    id: int
    order_id: int
    price: float
    
    class Config:
        from_attributes = True

