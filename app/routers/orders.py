from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.schemas.order import OrderCreate, OrderListResponse, OrderResponse, OrderUpdate, OrderStatus
from app.services.order_service import OrderService
from app.services.auth_service import AuthService
from app.models.customer import Customer

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
    # current_user: Customer = Depends(AuthService.get_current_customer)
):
    return OrderService.create_order(db, order_data)


@router.get("/", response_model=OrderListResponse)
async def get_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    customer_id: Optional[int] = None,
    status: Optional[OrderStatus] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    orders, total = OrderService.get_orders(
        db, skip, limit, customer_id, status, start_date, end_date
    )
    return {
        "total_records": total,
        "current_page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit,
        "data": orders
    }


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return OrderService.get_order(db, order_id)


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: int,
    order_data: OrderUpdate,
    db: Session = Depends(get_db)
):
    return OrderService.update_order(db, order_id, order_data)