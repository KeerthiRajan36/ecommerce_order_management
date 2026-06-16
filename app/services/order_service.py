from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from datetime import datetime
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.customer import Customer
from app.schemas.order import OrderCreate, OrderUpdate
from app.services.product_service import ProductService
from app.services.customer_service import CustomerService


class OrderService:
    @staticmethod
    def create_order(db: Session, order_data: OrderCreate) -> Order:
        
        customer = CustomerService.get_customer(db, order_data.customer_id)
        
        
        total_amount = 0.0
        order_items = []
        
        for item in order_data.items:
            
            product = ProductService.get_product(db, item.product_id)
            ProductService.check_stock(db, item.product_id, item.quantity)
            
            
            price = item.price if hasattr(item, 'price') and item.price else product.price
            
            order_items.append(
                OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=price
                )
            )
            total_amount += price * item.quantity
        
        
        db_order = Order(
            customer_id=order_data.customer_id,
            total_amount=total_amount,
            status=OrderStatus.PENDING
        )
        db.add(db_order)
        db.flush()  
        
        
        for item in order_items:
            item.order_id = db_order.id
            db.add(item)
            
            
            ProductService.reduce_stock(db, item.product_id, item.quantity)
        
        db.commit()
        db.refresh(db_order)
        
       
        return db.query(Order).options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.customer)
        ).filter(Order.id == db_order.id).first()
    
    @staticmethod
    def get_order(db: Session, order_id: int) -> Order:
        order = db.query(Order).options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.customer)
        ).filter(Order.id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        return order
    
    @staticmethod
    def get_orders(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        customer_id: Optional[int] = None,
        status: Optional[OrderStatus] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Tuple[List[Order], int]:
        query = db.query(Order).options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.customer)
        )
        
        if customer_id:
            query = query.filter(Order.customer_id == customer_id)
        
        if status:
            query = query.filter(Order.status == status)
        
        if start_date:
            query = query.filter(Order.order_date >= start_date)
        
        if end_date:
            query = query.filter(Order.order_date <= end_date)
        
        total = query.count()
        orders = query.order_by(Order.order_date.desc()).offset(skip).limit(limit).all()
        return orders, total
    
    @staticmethod
    def update_order(
        db: Session,
        order_id: int,
        order_data: OrderUpdate
    ) -> Order:
        order = OrderService.get_order(db, order_id)
        
        
        if order.status == OrderStatus.DELIVERED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Delivered orders cannot be modified"
            )
        
        if order.status == OrderStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cancelled orders cannot be modified"
            )
        
        if order_data.status == OrderStatus.CANCELLED:
            
            for item in order.items:
                product = ProductService.get_product(db, item.product_id)
                product.stock_quantity += item.quantity
                db.add(product)
        
        update_data = order_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(order, field, value)
        
        db.commit()
        db.refresh(order)
        return OrderService.get_order(db, order_id)
    
    @staticmethod
    def get_customer_orders(db: Session, customer_id: int) -> List[Order]:
        
        CustomerService.get_customer(db, customer_id)
        
        return db.query(Order).options(
            joinedload(Order.items).joinedload(OrderItem.product)
        ).filter(Order.customer_id == customer_id).order_by(Order.order_date.desc()).all()