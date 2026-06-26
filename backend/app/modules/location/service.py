from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Asset
from app.modules.location.models import AssetCreate

async def list_assets(db: AsyncSession) -> list[Asset]:
    result = await db.execute(select(Asset).order_by(Asset.created_at.desc()))
    return list(result.scalars().all())

async def get_asset(db: AsyncSession, asset_id: UUID) -> Asset | None:
    return await db.get(Asset, asset_id)

async def create_asset(db: AsyncSession, data: AssetCreate) -> Asset:
    asset = Asset(**data.model_dump())
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return asset