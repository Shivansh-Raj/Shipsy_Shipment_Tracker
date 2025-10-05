# app/schemas/shipment.py
from pydantic import BaseModel, Field, condecimal
from typing import Optional
from datetime import datetime
from app.models.shipment import ShipmentStatus

class ShipmentBase(BaseModel):
    description: str = Field(..., min_length=1)
    status: ShipmentStatus = ShipmentStatus.PENDING
    is_express: bool = False
    weight: float = Field(..., gt=0)
class ShipmentCreate(ShipmentBase):
    pass

class ShipmentUpdate(BaseModel):
    description: Optional[str]
    status: Optional[ShipmentStatus]
    is_express: Optional[bool]
    weight: Optional[float]

class ShipmentOut(ShipmentBase):
    id: int
    shipping_fee: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
