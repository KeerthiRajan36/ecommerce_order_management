from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import List, Optional


class CustomerBase(BaseModel):
    name : str =Field(...,min_length=1,max_length=100)
    email : EmailStr
    phone : Optional[str] = Field(None,max_length=20)
    address : Optional[str] = Field(None,max_length=255)

class CustomerCreate(CustomerBase):
    password:str = Field(...,min_length=6)

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class CustomerResponse(CustomerBase):
    id: int
    is_active : bool
    created_at : datetime
    updated_at : Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True
    )

class CustomerListResponse(BaseModel):

    total_records: int
    current_page: int
    limit: int
    data: List[CustomerResponse]
