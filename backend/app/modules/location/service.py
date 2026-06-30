from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.db.models import AccessPoint, Asset
from app.modules.location.models import APReading, AssetCreate, AssetUpdate

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

async def update_asset(db: AsyncSession, asset_id: UUID, data: AssetUpdate) -> Asset | None:
    asset = await db.get(Asset, asset_id)
    if asset is None:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(asset, field, value)
    await db.commit()
    await db.refresh(asset)
    return asset

async def delete_asset(db: AsyncSession, asset_id: UUID) -> bool:
    asset = await db.get(Asset, asset_id)
    if asset is None:
        return False
    await db.delete(asset)
    await db.commit()
    return True

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

async def record_asset_location(
    db: AsyncSession, asset: Asset, floor_plan_id: UUID, readings: list[APReading]
) -> Asset | None:
    """Resolve AP coordinates on the given floor, trilaterate, and persist.

    Returns the updated asset, or None when the readings are insufficient to
    compute a position (fewer than 3 readings match known access points).
    """
    result = await db.execute(
        select(AccessPoint).where(AccessPoint.floor_plan_id == floor_plan_id)
    )
    coords = {ap.mac_address: (ap.x, ap.y) for ap in result.scalars().all()}

    aps = [
        {"x": coords[r.mac_address][0], "y": coords[r.mac_address][1], "rssi": r.rssi}
        for r in readings
        if r.mac_address in coords
    ]

    position = calculate_position(aps)
    if position is None:
        return None

    asset.last_x, asset.last_y = position
    asset.last_floor_id = floor_plan_id
    asset.last_seen_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(asset)
    return asset