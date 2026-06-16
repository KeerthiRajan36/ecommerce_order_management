from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.auth_service  import AuthService


class CustomerService:
    @staticmethod
    def create_customer(db: Session, customer_data: CustomerCreate) -> Customer:
        # Check if email exists
        existing = db.query(Customer).filter(Customer.email == customer_data.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = AuthService.get_password_hash(customer_data.password)
        
        db_customer = Customer(
            name=customer_data.name,
            email=customer_data.email,
            phone=customer_data.phone,
            address=customer_data.address,
            # Note: In a real app, you'd store hashed_password in a separate User model
            # For simplicity, we'll just create the customer without storing password
        )
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    
    @staticmethod
    def get_customer(db: Session, customer_id: int) -> Customer:
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        return customer
    
    @staticmethod
    def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
        return db.query(Customer).filter(Customer.email == email).first()
    
    @staticmethod
    def get_customers(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None
    ) -> Tuple[List[Customer], int]:
        query = db.query(Customer)
        
        if search:
            query = query.filter(
                or_(
                    Customer.name.ilike(f"%{search}%"),
                    Customer.email.ilike(f"%{search}%")
                )
            )
        
        total = query.count()
        customers = query.offset(skip).limit(limit).all()
        return customers, total
    
    @staticmethod
    def update_customer(
        db: Session,
        customer_id: int,
        customer_data: CustomerUpdate
    ) -> Customer:
        customer = CustomerService.get_customer(db, customer_id)
        
        update_data = customer_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)
        
        db.commit()
        db.refresh(customer)
        return customer
    
    @staticmethod
    def delete_customer(db: Session, customer_id: int) -> None:
        customer = CustomerService.get_customer(db, customer_id)
        db.delete(customer)
        db.commit()