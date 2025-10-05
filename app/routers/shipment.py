from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.shipment import Shipment, ShipmentStatus
from app.schemas.shipment import ShipmentCreate, ShipmentOut, ShipmentUpdate
from app.routers.auth import get_current_user  

router = APIRouter(prefix="/shipments", tags=["Shipments"])

# Fee multipliers
EXPRESS_MULTIPLIER = 10.0
REGULAR_MULTIPLIER = 5.0

def calc_shipping_fee(weight: float, is_express: bool) -> float:
    multiplier = EXPRESS_MULTIPLIER if is_express else REGULAR_MULTIPLIER
    return round(weight * multiplier, 2)

@router.post("/", response_model=ShipmentOut, status_code=status.HTTP_201_CREATED)
def create_shipment(
    payload: ShipmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  
):
    fee = calc_shipping_fee(payload.weight, payload.is_express)
    db_obj = Shipment(description=payload.description,
        status=payload.status,
        is_express=payload.is_express,
        weight=payload.weight,
        shipping_fee=fee
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.get("/", response_model=List[ShipmentOut])
def list_shipments(
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1, le=100),
    status: Optional[ShipmentStatus] = None,
    is_express: Optional[bool] = None,
    search: Optional[str] = None,
    sort: Optional[str] = Query(None, description="e.g. shipping_fee or -created_at"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user) 
):
    skip = (page - 1) * limit
    q = db.query(Shipment)

    if status is not None:
        q = q.filter(Shipment.status == status)
    if is_express is not None:
        q = q.filter(Shipment.is_express == is_express)
    if search:
        q = q.filter(Shipment.description.ilike(f"%{search}%"))

    if sort:
        desc = sort.startswith("-")
        key = sort[1:] if desc else sort
        if key not in {"shipping_fee", "created_at", "weight"}:
            raise HTTPException(status_code=400, detail="Invalid sort field")
        column = getattr(Shipment, key)
        q = q.order_by(column.desc() if desc else column.asc())
    else:
        q = q.order_by(Shipment.created_at.desc())

    items = q.offset(skip).limit(limit).all()
    return items

@router.get("/{shipment_id}", response_model=ShipmentOut)
def get_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # JWT required
):
    obj = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return obj

@router.put("/{shipment_id}", response_model=ShipmentOut)
def update_shipment(
    shipment_id: int,
    payload: ShipmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # JWT required
):
    obj = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Shipment not found")

    changed_fee = False
    if payload.description is not None:
        obj.description = payload.description
    if payload.status is not None:
        obj.status = payload.status
    if payload.is_express is not None and payload.is_express != obj.is_express:
        obj.is_express = payload.is_express
        changed_fee = True
    if payload.weight is not None:
        if payload.weight <= 0:
            raise HTTPException(status_code=400, detail="weight must be > 0")
        obj.weight = payload.weight
        changed_fee = True

    if changed_fee:
        obj.shipping_fee = calc_shipping_fee(obj.weight, obj.is_express)

    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  
):
    obj = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Shipment not found")
    db.delete(obj)
    db.commit()
    return None
