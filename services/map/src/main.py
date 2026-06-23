from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import selectinload
from pathlib import Path
from uuid import UUID

from src.config import settings
from src.database import get_db
from src.models import FloorPlan, Zone, AccessPoint
from src.schemas import (
    FloorPlanCreate, FloorPlanResponse, FloorPlanSummary,
    ZoneCreate, ZoneResponse,
    AccessPointCreate, AccessPointResponse,
)

app = FastAPI(
    title="FloorSense Map Service",
    version="0.1.0",
    description="Floor plan and zone management",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent.parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# === Floor Plans ===

@app.get("/api/v1/maps", response_model=list[FloorPlanSummary])
async def list_floor_plans(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FloorPlan).order_by(FloorPlan.building, FloorPlan.floor))
    return result.scalars().all()

@app.post("/api/v1/maps", response_model=FloorPlanResponse, status_code=201)
async def create_floor_plan(payload: FloorPlanCreate, db: AsyncSession = Depends(get_db)):
    fp = FloorPlan(**payload.model_dump())
    db.add(fp)
    await db.commit()
    await db.refresh(fp)
    
    # Eagerly load relationships
    result = await db.execute(
        select(FloorPlan)
        .options(selectinload(FloorPlan.zones), selectinload(FloorPlan.access_points))
        .where(FloorPlan.id == fp.id)
    )
    return result.scalar_one()

@app.get("/api/v1/maps/{map_id}", response_model=FloorPlanResponse)
async def get_floor_plan(map_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(FloorPlan)
        .options(selectinload(FloorPlan.zones), selectinload(FloorPlan.access_points))
        .where(FloorPlan.id == map_id)
    )
    fp = result.scalar_one_or_none()
    if not fp:
        raise HTTPException(404, "Floor plan not found")
    return fp

# === Zones ===

@app.post("/api/v1/maps/{map_id}/zones", response_model=ZoneResponse, status_code=201)
async def create_zone(map_id: UUID, payload: ZoneCreate, db: AsyncSession = Depends(get_db)):
    fp = await db.get(FloorPlan, map_id)
    if not fp:
        raise HTTPException(404, "Floor plan not found")
    zone = Zone(floor_plan_id=map_id, **payload.model_dump())
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return zone

@app.get("/api/v1/maps/{map_id}/zones", response_model=list[ZoneResponse])
async def list_zones(map_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Zone).where(Zone.floor_plan_id == map_id))
    return result.scalars().all()

# === Access Points ===

@app.post("/api/v1/maps/{map_id}/aps", response_model=AccessPointResponse, status_code=201)
async def create_ap(map_id: UUID, payload: AccessPointCreate, db: AsyncSession = Depends(get_db)):
    fp = await db.get(FloorPlan, map_id)
    if not fp:
        raise HTTPException(404, "Floor plan not found")
    ap = AccessPoint(floor_plan_id=map_id, **payload.model_dump())
    db.add(ap)
    await db.commit()
    await db.refresh(ap)
    return ap

@app.get("/api/v1/maps/{map_id}/aps", response_model=list[AccessPointResponse])
async def list_aps(map_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AccessPoint).where(AccessPoint.floor_plan_id == map_id))
    return result.scalars().all()

# === Health ===

@app.get("/health")
async def health():
    return {"status": "ok", "service": "map"}