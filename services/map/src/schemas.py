from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional

class ZoneCreate(BaseModel):
    name: str
    zone_type: str = "general"
    polygon: list[list[float]] = Field(..., description="Array of [x, y] coordinates")

class ZoneResponse(ZoneCreate):
    id: UUID
    floor_plan_id: UUID
    
    class Config:
        from_attributes = True

class AccessPointCreate(BaseModel):
    mac_address: str
    name: Optional[str] = None
    x: float
    y: float

class AccessPointResponse(AccessPointCreate):
    id: UUID
    floor_plan_id: UUID
    
    class Config:
        from_attributes = True

class FloorPlanCreate(BaseModel):
    name: str
    building: str
    floor: str
    svg_url: Optional[str] = None
    image_url: Optional[str] = None
    width: float
    height: float

class FloorPlanResponse(FloorPlanCreate):
    id: UUID
    zones: list[ZoneResponse] = []
    access_points: list[AccessPointResponse] = []
    
    class Config:
        from_attributes = True

class FloorPlanSummary(BaseModel):
    id: UUID
    name: str
    building: str
    floor: str
    
    class Config:
        from_attributes = True