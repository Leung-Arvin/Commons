from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import FloorPlan
from app.modules.map.models import FloorPlanCreate

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