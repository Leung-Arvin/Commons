from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AccessPoint, FloorPlan, Zone
from app.modules.map.models import (
    AccessPointCreate,
    AccessPointUpdate,
    FloorPlanCreate,
    FloorPlanUpdate,
    ZoneCreate,
    ZoneUpdate,
)

async def list_floor_plans(db: AsyncSession) -> list[FloorPlan]:
    result = await db.execute(select(FloorPlan).order_by(FloorPlan.created_at.desc()))
    return list(result.scalars().all())

async def get_floor_plan(db: AsyncSession, floor_id: UUID) -> FloorPlan | None:
    return await db.get(FloorPlan, floor_id)

async def create_floor_plan(db: AsyncSession, data: FloorPlanCreate) -> FloorPlan:
    fp = FloorPlan(**data.model_dump())
    db.add(fp)
    await db.commit()
    await db.refresh(fp)
    return fp

async def update_floor_plan(
    db: AsyncSession, floor_id: UUID, data: FloorPlanUpdate
) -> FloorPlan | None:
    fp = await db.get(FloorPlan, floor_id)
    if fp is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(fp, field, value)
    await db.commit()
    await db.refresh(fp)
    return fp

async def delete_floor_plan(db: AsyncSession, floor_id: UUID) -> bool:
    fp = await db.get(FloorPlan, floor_id)
    if fp is None:
        return False
    await db.delete(fp)
    await db.commit()
    return True

async def create_zone(db: AsyncSession, map_id: UUID, data: ZoneCreate) -> Zone:
    zone = Zone(floor_plan_id=map_id, **data.model_dump())
    db.add(zone)
    await db.commit()
    await db.refresh(zone)
    return zone

async def list_zones(db: AsyncSession, map_id: UUID) -> list[Zone]:
    result = await db.execute(select(Zone).where(Zone.floor_plan_id == map_id))
    return list(result.scalars().all())


async def update_zone(
    db: AsyncSession, map_id: UUID, zone_id: UUID, data: ZoneUpdate
) -> Zone | None:
    zone = await db.get(Zone, zone_id)
    if zone is None or zone.floor_plan_id != map_id:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(zone, field, value)
    await db.commit()
    await db.refresh(zone)
    return zone


async def delete_zone(db: AsyncSession, map_id: UUID, zone_id: UUID) -> bool:
    zone = await db.get(Zone, zone_id)
    if zone is None or zone.floor_plan_id != map_id:
        return False
    await db.delete(zone)
    await db.commit()
    return True

async def create_access_point(db: AsyncSession, map_id: UUID, data: AccessPointCreate) -> AccessPoint:
    ap = AccessPoint(floor_plan_id=map_id, **data.model_dump())
    db.add(ap)
    await db.commit()
    await db.refresh(ap)
    return ap

async def list_access_points(db: AsyncSession, map_id: UUID) -> list[AccessPoint]:
    result = await db.execute(select(AccessPoint).where(AccessPoint.floor_plan_id == map_id))
    return list(result.scalars().all())


async def update_access_point(
    db: AsyncSession, map_id: UUID, ap_id: UUID, data: AccessPointUpdate
) -> AccessPoint | None:
    ap = await db.get(AccessPoint, ap_id)
    if ap is None or ap.floor_plan_id != map_id:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(ap, field, value)
    await db.commit()
    await db.refresh(ap)
    return ap


async def delete_access_point(db: AsyncSession, map_id: UUID, ap_id: UUID) -> bool:
    ap = await db.get(AccessPoint, ap_id)
    if ap is None or ap.floor_plan_id != map_id:
        return False
    await db.delete(ap)
    await db.commit()
    return True