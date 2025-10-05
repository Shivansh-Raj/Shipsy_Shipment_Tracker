
import enum
from sqlalchemy import Column, Integer, String, Boolean, Float, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base

# Enum to represent the shipment status
class ShipmentStatus(str, enum.Enum):
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"

# Shipment main model
class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(Enum(ShipmentStatus), default=ShipmentStatus.PENDING, nullable=False)
    is_express = Column(Boolean, default=False, nullable=False)
    weight = Column(Float, nullable=False)
    shipping_fee = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
