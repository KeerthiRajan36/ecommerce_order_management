from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    @staticmethod
    def create_product(db: Session, product_data: ProductCreate) -> Product:
        db_product = Product(**product_data.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def get_product(db: Session, product_id: int) :
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return product
    
    @staticmethod
    def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        search: Optional[str] = None,
        active_only: bool = True
    ):
        query = db.query(Product)
        
        if active_only:
            query = query.filter(Product.is_active == True)
        
        if category:
            query = query.filter(Product.category == category)
        
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%")
                )
            )
        
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        return products, total
    
    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_data: ProductUpdate
    ) -> Product:
        product = ProductService.get_product(db, product_id)
        
        update_data = product_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> None:
        product = ProductService.get_product(db, product_id)
        db.delete(product)
        db.commit()
    
    @staticmethod
    def check_stock(db: Session, product_id: int, quantity: int) -> bool:
        product = ProductService.get_product(db, product_id)
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product '{product.name}' is inactive"
            )
        if product.stock_quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for '{product.name}'. Available: {product.stock_quantity}"
            )
        return True
    
    @staticmethod
    def reduce_stock(db: Session, product_id: int, quantity: int) -> Product:
        product = ProductService.get_product(db, product_id)
        if product.stock_quantity < quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for '{product.name}'"
            )
        product.stock_quantity -= quantity
        db.commit()
        db.refresh(product)
        return product