import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class FloorPlan(Base):
    __tablename__ = "floor_plans"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=False)
    width_m: Mapped[float] = mapped_column(Float, nullable=False)
    height_m: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class Asset(Base):
    __tablename__ = "assets"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    mac_address: Mapped[str] = mapped_column(String(17), unique=True, nullable=False, index=True)
    asset_type: Mapped[str] = mapped_column(String(50), default="unknown")  # laptop, phone, ap, etc.
    last_x: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_y: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    last_floor_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), nullable=True)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())