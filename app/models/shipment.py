from sqlalchemy import Column, Integer, String, Boolean, Float, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base
import enum

class ShipmentStatus(str, enum.Enum):
    PENDING = "Pending"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(Enum(ShipmentStatus), default=ShipmentStatus.PENDING)
    is_express = Column(Boolean, default=False)
    weight = Column(Float, nullable=False)
    shipping_fee = Column(Float)  # calculated field
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
