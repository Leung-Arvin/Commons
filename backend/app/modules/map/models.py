from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ZoneCreate(BaseModel):
    name: str
    zone_type: str = "general"
    polygon: list[list[float]]


class ZoneUpdate(BaseModel):
    name: Optional[str] = None
    zone_type: Optional[str] = None
    polygon: Optional[list[list[float]]] = None


class ZoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    floor_plan_id: UUID
    name: str
    zone_type: str = "general"
    polygon: list[list[float]]


class AccessPointCreate(BaseModel):
    mac_address: str
    name: Optional[str] = None
    x: float
    y: float


class AccessPointUpdate(BaseModel):
    mac_address: Optional[str] = None
    name: Optional[str] = None
    x: Optional[float] = None
    y: Optional[float] = None


class AccessPointResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    floor_plan_id: UUID
    mac_address: str
    name: Optional[str] = None
    x: float
    y: float


class FloorPlanCreate(BaseModel):
    name: str
    building: str
    floor: str
    svg_url: Optional[str] = None
    image_url: Optional[str] = None
    width: float
    height: float


class FloorPlanUpdate(BaseModel):
    name: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[str] = None
    svg_url: Optional[str] = None
    image_url: Optional[str] = None
    width: Optional[float] = None
    height: Optional[float] = None


class FloorPlanSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    building: str
    floor: str


class FloorPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    building: str
    floor: str
    svg_url: Optional[str] = None
    image_url: Optional[str] = None
    width: float
    height: float
    zones: list[ZoneResponse] = []
    access_points: list[AccessPointResponse] = []
