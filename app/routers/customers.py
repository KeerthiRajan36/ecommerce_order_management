from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional,List
from app.database import get_db
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate ,CustomerListResponse
from app.services.customer_service import CustomerService
from app.services.auth_service import AuthService

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    return CustomerService.create_customer(db, customer_data)


@router.get("/", response_model=CustomerListResponse)
async def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    customers, total = CustomerService.get_customers(db, skip, limit, search)
    
    return {
        "total_records": total,
        "current_page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit,
        "data": customers
    }


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return CustomerService.get_customer(db, customer_id)


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    return CustomerService.update_customer(db, customer_id, customer_data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    CustomerService.delete_customer(db, customer_id)


@router.get("/{customer_id}/orders", response_model=list)
async def get_customer_orders(
    customer_id: int,
    db: Session = Depends(get_db)
):
    from app.services.order_service import OrderService
    return OrderService.get_customer_orders(db, customer_id)