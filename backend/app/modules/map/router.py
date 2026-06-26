from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.map.models import FloorPlanCreate, FloorPlanRead
from app.modules.map import service

router = APIRouter(prefix="/maps", tags=["maps"])

@router.get("/", response_model=list[FloorPlanRead])
async def list_maps(db: AsyncSession = Depends(get_db)):
    return await service.list_floor_plans(db)

@router.post("/", response_model=FloorPlanRead, status_code=201)
async def create_map(data: FloorPlanCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_floor_plan(db, data)

@router.get("/{floor_id}", response_model=FloorPlanRead)
async def get_map(floor_id: UUID, db: AsyncSession = Depends(get_db)):
    fp = await service.get_floor_plan(db, floor_id)
    if not fp:
        raise HTTPException(status_code=404, detail="Floor plan not found")
    return fp