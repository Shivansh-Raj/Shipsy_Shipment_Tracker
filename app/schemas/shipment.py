from pydantic import BaseModel
from typing import Optional
from app.models.shipment import ShipmentStatus

class ShipmentBase(BaseModel):
    description: str
    status: ShipmentStatus
    is_express: bool
    weight: float

class ShipmentCreate(ShipmentBase):
    pass

class ShipmentOut(ShipmentBase):
    id: int
    shipping_fee: float
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
