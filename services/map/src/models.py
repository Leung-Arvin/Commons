from sqlalchemy import Column, String, Float, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, DeclarativeBase
import uuid

class Base(DeclarativeBase):
    pass

class FloorPlan(Base):
    __tablename__ = "floor_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    building = Column(String, nullable=False)
    floor = Column(String, nullable=False)
    svg_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    width = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    
    zones = relationship("Zone", back_populates="floor_plan", cascade="all, delete-orphan")
    access_points = relationship("AccessPoint", back_populates="floor_plan", cascade="all, delete-orphan")

class Zone(Base):
    __tablename__ = "zones"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    floor_plan_id = Column(UUID(as_uuid=True), ForeignKey("floor_plans.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    zone_type = Column(String, default="general")  # general, meeting_room, desk_area, etc.
    polygon = Column(JSON, nullable=False)  # [[x1,y1], [x2,y2], ...]
    
    floor_plan = relationship("FloorPlan", back_populates="zones")

class AccessPoint(Base):
    __tablename__ = "access_points"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    floor_plan_id = Column(UUID(as_uuid=True), ForeignKey("floor_plans.id", ondelete="CASCADE"), nullable=False)
    mac_address = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    
    floor_plan = relationship("FloorPlan", back_populates="access_points")