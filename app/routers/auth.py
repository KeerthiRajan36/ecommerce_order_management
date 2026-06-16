from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.models.customer import Customer
from app.schemas.auth import Token, UserLogin, UserRegister
from app.services.auth_service import AuthService
from app.services.customer_service import CustomerService
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Token)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    
    existing = CustomerService.get_customer_by_email(db, user_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    
    customer = Customer(
        name=user_data.name,
        email=user_data.email,
        phone=user_data.phone,
        address=user_data.address
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    

    access_token = AuthService.create_access_token(
        data={"sub": str(customer.id), "email": customer.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    
    customer = CustomerService.get_customer_by_email(db, login_data.email)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = AuthService.create_access_token(
        data={"sub": str(customer.id), "email": customer.email}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}