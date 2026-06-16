from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Tuple
from fastapi import HTTPException, status
from datetime import datetime
from app.models.shipment import Shipment, ShipmentStatus
from app.models.order import Order, OrderStatus
from app.services.order_service import OrderService


class ShipmentService:
    @staticmethod
    def create_shipment(db: Session, shipment_data) -> Shipment:
        # Validate order exists
        order = OrderService.get_order(db, shipment_data.order_id)
        
        # Check if shipment already exists
        existing = db.query(Shipment).filter(Shipment.order_id == shipment_data.order_id).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A shipment already exists for this order"
            )
        
        # Check if tracking number is unique
        tracking_exists = db.query(Shipment).filter(
            Shipment.tracking_number == shipment_data.tracking_number
        ).first()
        if tracking_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tracking number already exists"
            )
        
        # Check if order can be shipped
        if order.status == OrderStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create shipment for cancelled order"
            )
        
        db_shipment = Shipment(
            order_id=shipment_data.order_id,
            tracking_number=shipment_data.tracking_number,
            status=ShipmentStatus.PENDING
        )
        db.add(db_shipment)
        
        # Update order status
        order.status = OrderStatus.SHIPPED
        db.add(order)
        
        db.commit()
        db.refresh(db_shipment)
        
        return db.query(Shipment).options(
            joinedload(Shipment.order)
        ).filter(Shipment.id == db_shipment.id).first()
    
    @staticmethod
    def get_shipment(db: Session, shipment_id: int) -> Shipment:
        shipment = db.query(Shipment).options(
            joinedload(Shipment.order)
        ).filter(Shipment.id == shipment_id).first()
        
        if not shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shipment not found"
            )
        return shipment
    
    @staticmethod
    def get_shipment_by_tracking(db: Session, tracking_number: str) -> Optional[Shipment]:
        return db.query(Shipment).filter(Shipment.tracking_number == tracking_number).first()
    
    @staticmethod
    def get_shipments(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ShipmentStatus] = None,
        order_id: Optional[int] = None
    ) -> Tuple[List[Shipment], int]:
        query = db.query(Shipment).options(joinedload(Shipment.order))
        
        if status:
            query = query.filter(Shipment.status == status)
        
        if order_id:
            query = query.filter(Shipment.order_id == order_id)
        
        total = query.count()
        shipments = query.order_by(Shipment.created_at.desc()).offset(skip).limit(limit).all()
        return shipments, total
    
    @staticmethod
    def update_shipment(
        db: Session,
        shipment_id: int,
        shipment_data
    ) -> Shipment:
        shipment = ShipmentService.get_shipment(db, shipment_id)
        order = shipment.order
        
        # Check if tracking number is unique (if changing)
        if (shipment_data.tracking_number and 
            shipment_data.tracking_number != shipment.tracking_number):
            tracking_exists = db.query(Shipment).filter(
                Shipment.tracking_number == shipment_data.tracking_number
            ).first()
            if tracking_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Tracking number already exists"
                )
        
        # Update status and timestamps
        if shipment_data.status:
            old_status = shipment.status
            shipment.status = shipment_data.status
            
            if shipment_data.status == ShipmentStatus.SHIPPED and not shipment.shipped_date:
                shipment.shipped_date = datetime.utcnow()
                # Update order status
                order.status = OrderStatus.SHIPPED
            elif shipment_data.status == ShipmentStatus.DELIVERED and not shipment.delivered_date:
                shipment.delivered_date = datetime.utcnow()
                # Update order status
                order.status = OrderStatus.DELIVERED
            
            db.add(order)
        
        update_data = shipment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field != 'status':  # Already handled
                setattr(shipment, field, value)
        
        db.commit()
        db.refresh(shipment)
        return ShipmentService.get_shipment(db, shipment_id)
    
    @staticmethod
    def delete_shipment(db: Session, shipment_id: int) -> None:
        shipment = ShipmentService.get_shipment(db, shipment_id)
        db.delete(shipment)
        db.commit()