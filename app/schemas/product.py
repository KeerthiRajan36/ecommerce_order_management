from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from pydantic.v1 import ConfigDict

class ProductBase(BaseModel):
    name:str = Field(...,min_length=1,max_length=200)
    description:Optional[str] = Field(None,max_length=1000) 
    price :float =Field(...,gt=0)
    stock_quantity :int = Field(...,ge=0)
    category:Optional[str] = Field(None,max_length=100)


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name:Optional[str] =Field(None,min_length=1,max_length=200)
    description:Optional[str] = Field(None,max_length=1000)
    price:Optional[float] = Field(None,gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = ConfigDict(
        from_attributes=True
    )

class ProductListResponse(BaseModel):
    total_records: int
    current_page: int
    limit: int
    data: list[ProductResponse]