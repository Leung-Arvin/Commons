from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

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

def calculate_position(aps: list[dict]) -> Optional[tuple[float, float]]:
    """
    Calculate X/Y position using Weighted Centroid.
    Weight is inversely proportional to signal strength (stronger signal = higher weight).
    """
    if len(aps) < 3:
        return None

    total_weight = 0.0
    weighted_x = 0.0
    weighted_y = 0.0

    for ap in aps:
        rssi = ap["rssi"]
        if rssi == 0:
            continue  # Skip invalid data
        
        weight = 1.0 / abs(rssi)
        weighted_x += ap["x"] * weight
        weighted_y += ap["y"] * weight
        total_weight += weight

    if total_weight == 0:
        return None

    x = weighted_x / total_weight
    y = weighted_y / total_weight

    return (x, y)