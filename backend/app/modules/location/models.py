from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class AssetCreate(BaseModel):
    name: str
    mac_address: str
    asset_type: str = "unknown"

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    asset_type: Optional[str] = None

class APReading(BaseModel):
    mac_address: str
    rssi: float

class LocateRequest(BaseModel):
    floor_plan_id: UUID
    readings: list[APReading]

class AssetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    mac_address: str
    asset_type: str
    last_x: Optional[float]
    last_y: Optional[float]
    last_floor_id: Optional[UUID]
    last_seen_at: Optional[datetime]
    created_at: datetime