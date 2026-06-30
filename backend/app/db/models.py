import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class FloorPlan(Base):
    __tablename__ = "floor_plans"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    building: Mapped[str] = mapped_column(String(200), nullable=False)
    floor: Mapped[str] = mapped_column(String(50), nullable=False)
    svg_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    width: Mapped[float] = mapped_column(Float, nullable=False)
    height: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    zones: Mapped[list["Zone"]] = relationship(
        "Zone", lazy="selectin", cascade="all, delete-orphan"
    )
    access_points: Mapped[list["AccessPoint"]] = relationship(
        "AccessPoint", lazy="selectin", cascade="all, delete-orphan"
    )

class Zone(Base):
    __tablename__ = "zones"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    floor_plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("floor_plans.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    zone_type: Mapped[str] = mapped_column(String(50), default="general", nullable=False)
    polygon: Mapped[list] = mapped_column(JSON, nullable=False)  # [[x, y], ...]
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class AccessPoint(Base):
    __tablename__ = "access_points"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    floor_plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("floor_plans.id"), nullable=False, index=True
    )
    mac_address: Mapped[str] = mapped_column(String(17), nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    x: Mapped[float] = mapped_column(Float, nullable=False)
    y: Mapped[float] = mapped_column(Float, nullable=False)
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