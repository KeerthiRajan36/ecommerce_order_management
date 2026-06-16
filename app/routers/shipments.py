from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.shipment import ShipmentCreate, ShipmentListResponse, ShipmentResponse, ShipmentUpdate, ShipmentStatus
from app.services.shipment_service import ShipmentService
from app.services.auth_service import AuthService
from app.models.customer import Customer

router = APIRouter(prefix="/shipments", tags=["Shipments"])


@router.post("/", response_model=ShipmentResponse, status_code=status.HTTP_201_CREATED)
async def create_shipment(
    shipment_data: ShipmentCreate,
    db: Session = Depends(get_db),
    current_user: Customer = Depends(AuthService.get_current_customer)
):
    return ShipmentService.create_shipment(db, shipment_data)


@router.get("/", response_model=ShipmentListResponse)
async def get_shipments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[ShipmentStatus] = None,
    order_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    shipments, total = ShipmentService.get_shipments(db, skip, limit, status, order_id)
    return {
        "total_records": total,
        "current_page": skip // limit + 1 if limit > 0 else 1,
        "limit": limit,
        "data": shipments
    }


@router.get("/{shipment_id}", response_model=ShipmentResponse)
async def get_shipment(
    shipment_id: int,
    db: Session = Depends(get_db)
):
    return ShipmentService.get_shipment(db, shipment_id)


@router.put("/{shipment_id}", response_model=ShipmentResponse)
async def update_shipment(
    shipment_id: int,
    shipment_data: ShipmentUpdate,
    db: Session = Depends(get_db)
):
    return ShipmentService.update_shipment(db, shipment_id, shipment_data)


@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shipment(
    shipment_id: int,
    db: Session = Depends(get_db)
):
    ShipmentService.delete_shipment(db, shipment_id)