from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.shipment import Shipment, ShipmentStatus
from app.schemas.shipment import ShipmentCreate, ShipmentOut, ShipmentUpdate
from app.routers.auth import get_authenticated_user

router = APIRouter(prefix="/shipments", tags=["Shipments"])


# Fee Multiplier to calculate shipment fees
EXPRESS_RATE = 12.0
STANDARD_RATE = 7.0

def compute_fee(weight: float, express: bool) -> float:
    """Calculates shipping fee based on weight and shipping type."""
    rate = EXPRESS_RATE if express else STANDARD_RATE
    return round(weight * rate, 2)


# Shipment Endpoints

@router.post("/", response_model=ShipmentOut, status_code=status.HTTP_201_CREATED)
def add_shipment(
    shipment_data: ShipmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_authenticated_user)
):
    fee = compute_fee(shipment_data.weight, shipment_data.is_express)
    shipment = Shipment(
        description=shipment_data.description,
        status=shipment_data.status,
        is_express=shipment_data.is_express,
        weight=shipment_data.weight,
        shipping_fee=fee
    )
    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment

@router.get("/", response_model=List[ShipmentOut])
def fetch_shipments(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),
    status_filter: Optional[ShipmentStatus] = None,
    express_filter: Optional[bool] = None,
    search_term: Optional[str] = None,
    order_by: Optional[str] = Query(None, description="e.g. shipping_fee or -created_at"),
    db: Session = Depends(get_db),
    current_user = Depends(get_authenticated_user)
):
    offset = (page - 1) * limit
    query = db.query(Shipment)

    if status_filter is not None:
        query = query.filter(Shipment.status == status_filter)
    if express_filter is not None:
        query = query.filter(Shipment.is_express == express_filter)
    if search_term:
        query = query.filter(Shipment.description.ilike(f"%{search_term}%"))

    if order_by:
        descending = order_by.startswith("-")
        field_name = order_by[1:] if descending else order_by
        if field_name not in {"shipping_fee", "weight", "created_at"}:
            raise HTTPException(status_code=400, detail="Invalid sorting field")
        column = getattr(Shipment, field_name)
        query = query.order_by(column.desc() if descending else column.asc())
    else:
        query = query.order_by(Shipment.created_at.desc())

    return query.offset(offset).limit(limit).all()

@router.get("/{shipment_id}", response_model=ShipmentOut)
def get_shipment_detail(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_authenticated_user)
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

@router.put("/{shipment_id}", response_model=ShipmentOut)
def modify_shipment(
    shipment_id: int,
    updates: ShipmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_authenticated_user)
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    fee_needs_update = False
    if updates.description is not None:
        shipment.description = updates.description
    if updates.status is not None:
        shipment.status = updates.status
    if updates.is_express is not None and updates.is_express != shipment.is_express:
        shipment.is_express = updates.is_express
        fee_needs_update = True
    if updates.weight is not None:
        if updates.weight <= 0:
            raise HTTPException(status_code=400, detail="Weight must be positive")
        shipment.weight = updates.weight
        fee_needs_update = True

    if fee_needs_update:
        shipment.shipping_fee = compute_fee(shipment.weight, shipment.is_express)

    db.add(shipment)
    db.commit()
    db.refresh(shipment)
    return shipment

@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_authenticated_user)
):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    db.delete(shipment)
    db.commit()
    return None
