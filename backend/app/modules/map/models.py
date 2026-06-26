from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class FloorPlanCreate(BaseModel):
    name: str
    image_url: str
    width_m: float
    height_m: float

class FloorPlanRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    name: str
    image_url: str
    width_m: float
    height_m: float
    created_at: datetime