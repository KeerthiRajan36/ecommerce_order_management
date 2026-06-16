from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.product import ProductCreate, ProductListResponse, ProductResponse, ProductUpdate
from app.services.product_service import ProductService
from app.services.auth_service import AuthService
from app.models.customer import Customer

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(AuthService.get_current_customer)
):
    
    return ProductService.create_product(db, product_data)


@router.get("/", response_model=ProductListResponse)
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    search: Optional[str] = None,
    active_only: bool = Query(True),
    db: Session = Depends(get_db)
):
    products, total = ProductService.get_products(
        db, skip, limit, category, search, active_only
    )
    return {
        "total_records": total,
        "current_page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit,
        "data": products
    }


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return ProductService.get_product(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    return ProductService.update_product(db, product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    ProductService.delete_product(db, product_id)