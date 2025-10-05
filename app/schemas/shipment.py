
from pydantic import BaseModel, Field, condecimal
from typing import Optional
from datetime import datetime
from app.models.shipment import ShipmentStatus

# Base model for shipment 
class ShipmentBase(BaseModel):
    description: str = Field(..., min_length=1)
    status: ShipmentStatus = ShipmentStatus.PENDING
    is_express: bool = False
    weight: float = Field(..., gt=0)

# Model that creates new shipment
class ShipmentCreate(ShipmentBase):
    pass

# Model that updates a shipment
class ShipmentUpdate(BaseModel):
    description: Optional[str]
    status: Optional[ShipmentStatus]
    is_express: Optional[bool]
    weight: Optional[float]

# Model that provides and output for a shipment
class ShipmentOut(ShipmentBase):
    id: int
    shipping_fee: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
