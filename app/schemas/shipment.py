from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional,List
import enum


class ShipmentStatus(str, enum.Enum):
    PENDING = "pending"
    PACKED = "packed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"


class ShipmentBase(BaseModel):
    order_id: int
    tracking_number: str = Field(..., min_length=1, max_length=100)


class ShipmentCreate(ShipmentBase):
    pass


class ShipmentUpdate(BaseModel):
    status: Optional[ShipmentStatus] = None
    tracking_number: Optional[str] = Field(None, min_length=1, max_length=100)


class ShipmentResponse(ShipmentBase):
    id: int
    status: ShipmentStatus
    shipped_date: Optional[datetime]
    delivered_date: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ShipmentListResponse(BaseModel):
    total_records: int
    current_page: int
    limit: int
    data: List[ShipmentResponse]