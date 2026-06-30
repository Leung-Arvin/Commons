from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.map.models import (
    AccessPointCreate,
    AccessPointResponse,
    AccessPointUpdate,
    FloorPlanCreate,
    FloorPlanResponse,
    FloorPlanSummary,
    FloorPlanUpdate,
    ZoneCreate,
    ZoneResponse,
    ZoneUpdate,
)
from app.modules.map import service

router = APIRouter(prefix="/maps", tags=["maps"])

@router.get("/", response_model=list[FloorPlanSummary])
async def list_maps(db: AsyncSession = Depends(get_db)):
    return await service.list_floor_plans(db)

@router.post("/", response_model=FloorPlanResponse, status_code=201)
async def create_map(data: FloorPlanCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_floor_plan(db, data)

@router.get("/{floor_id}", response_model=FloorPlanResponse)
async def get_map(floor_id: UUID, db: AsyncSession = Depends(get_db)):
    fp = await service.get_floor_plan(db, floor_id)
    if not fp:
        raise HTTPException(status_code=404, detail="Floor plan not found")
    return fp

@router.put("/{floor_id}", response_model=FloorPlanResponse)
async def update_map(floor_id: UUID, data: FloorPlanUpdate, db: AsyncSession = Depends(get_db)):
    fp = await service.update_floor_plan(db, floor_id, data)
    if not fp:
        raise HTTPException(status_code=404, detail="Floor plan not found")
    return fp

@router.delete("/{floor_id}", status_code=204)
async def delete_map(floor_id: UUID, db: AsyncSession = Depends(get_db)):
    if not await service.delete_floor_plan(db, floor_id):
        raise HTTPException(status_code=404, detail="Floor plan not found")

@router.post("/{map_id}/zones", response_model=ZoneResponse, status_code=201)
async def create_zone(map_id: UUID, data: ZoneCreate, db: AsyncSession = Depends(get_db)):
    if not await service.get_floor_plan(db, map_id):
        raise HTTPException(status_code=404, detail="Floor plan not found")
    return await service.create_zone(db, map_id, data)

@router.get("/{map_id}/zones", response_model=list[ZoneResponse])
async def list_zones(map_id: UUID, db: AsyncSession = Depends(get_db)):
    return await service.list_zones(db, map_id)

@router.put("/{map_id}/zones/{zone_id}", response_model=ZoneResponse)
async def update_zone(map_id: UUID, zone_id: UUID, data: ZoneUpdate, db: AsyncSession = Depends(get_db)):
    zone = await service.update_zone(db, map_id, zone_id, data)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    return zone

@router.delete("/{map_id}/zones/{zone_id}", status_code=204)
async def delete_zone(map_id: UUID, zone_id: UUID, db: AsyncSession = Depends(get_db)):
    if not await service.delete_zone(db, map_id, zone_id):
        raise HTTPException(status_code=404, detail="Zone not found")

@router.post("/{map_id}/aps", response_model=AccessPointResponse, status_code=201)
async def create_access_point(map_id: UUID, data: AccessPointCreate, db: AsyncSession = Depends(get_db)):
    if not await service.get_floor_plan(db, map_id):
        raise HTTPException(status_code=404, detail="Floor plan not found")
    return await service.create_access_point(db, map_id, data)

@router.get("/{map_id}/aps", response_model=list[AccessPointResponse])
async def list_access_points(map_id: UUID, db: AsyncSession = Depends(get_db)):
    return await service.list_access_points(db, map_id)

@router.put("/{map_id}/aps/{ap_id}", response_model=AccessPointResponse)
async def update_access_point(map_id: UUID, ap_id: UUID, data: AccessPointUpdate, db: AsyncSession = Depends(get_db)):
    ap = await service.update_access_point(db, map_id, ap_id, data)
    if not ap:
        raise HTTPException(status_code=404, detail="Access point not found")
    return ap

@router.delete("/{map_id}/aps/{ap_id}", status_code=204)
async def delete_access_point(map_id: UUID, ap_id: UUID, db: AsyncSession = Depends(get_db)):
    if not await service.delete_access_point(db, map_id, ap_id):
        raise HTTPException(status_code=404, detail="Access point not found")
