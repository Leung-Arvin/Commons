"""Seed the database with a demo floor plan for local development.

Idempotent: running it repeatedly removes the previously-seeded demo data
(matched by a stable marker) and recreates it, so you always get a clean,
predictable floor plan. Non-demo data is left untouched.

Usage:
    python -m app.seed            # from the backend/ directory (venv active)
    make seed                     # from the repo root

Requires the database to be running and migrated first:
    (cd deploy && docker compose up -d postgres) && alembic upgrade head
"""

import asyncio
from datetime import datetime, timezone

from sqlalchemy import delete, select

from app.database import async_session
from app.db.models import AccessPoint, Asset, FloorPlan, Zone

# Stable markers so re-seeding only touches demo rows.
DEMO_BUILDING = "Solace HQ"
DEMO_NAME = "Demo — West Wing"
DEMO_ASSET_PREFIX = "DE:MO:"

# Floor-plan coordinate space (pixels). Zones/APs/assets are positioned in here.
WIDTH = 1040.0
HEIGHT = 600.0

ZONES = [
    {"name": "Boardroom", "zone_type": "meeting_room",
     "polygon": [[60, 60], [360, 60], [360, 240], [60, 240]]},
    {"name": "Focus Room", "zone_type": "meeting_room",
     "polygon": [[400, 60], [620, 60], [620, 240], [400, 240]]},
    {"name": "Engineering", "zone_type": "desk_area",
     "polygon": [[60, 280], [500, 280], [500, 540], [60, 540]]},
    {"name": "Sales Pod", "zone_type": "desk_area",
     "polygon": [[660, 60], [980, 60], [980, 300], [660, 300]]},
    {"name": "Lounge", "zone_type": "general",
     "polygon": [[540, 340], [980, 340], [980, 540], [540, 540]]},
]

ACCESS_POINTS = [
    {"mac_address": "AP:00:00:00:00:01", "name": "AP-01", "x": 200, "y": 150},
    {"mac_address": "AP:00:00:00:00:02", "name": "AP-02", "x": 510, "y": 150},
    {"mac_address": "AP:00:00:00:00:03", "name": "AP-03", "x": 280, "y": 410},
    {"mac_address": "AP:00:00:00:00:04", "name": "AP-04", "x": 820, "y": 180},
    {"mac_address": "AP:00:00:00:00:05", "name": "AP-05", "x": 760, "y": 440},
]

# Assets carry a live position so the Devices / Assets layers have something to show.
ASSETS = [
    {"name": "Laptop-7F3A", "asset_type": "laptop",
     "mac_address": "DE:MO:00:00:01", "last_x": 150, "last_y": 360},
    {"name": "Phone-22B1", "asset_type": "phone",
     "mac_address": "DE:MO:00:00:02", "last_x": 300, "last_y": 120},
    {"name": "Tablet-9C0E", "asset_type": "tablet",
     "mac_address": "DE:MO:00:00:03", "last_x": 720, "last_y": 420},
    {"name": "Scanner-4471", "asset_type": "scanner",
     "mac_address": "DE:MO:00:00:04", "last_x": 820, "last_y": 150},
]


async def _clear_demo(session) -> None:
    """Remove previously-seeded demo rows (zones/APs cascade with the floor plan)."""
    existing = await session.execute(
        select(FloorPlan).where(
            FloorPlan.building == DEMO_BUILDING, FloorPlan.name == DEMO_NAME
        )
    )
    for fp in existing.scalars().all():
        await session.delete(fp)
    await session.execute(
        delete(Asset).where(Asset.mac_address.like(f"{DEMO_ASSET_PREFIX}%"))
    )
    await session.commit()


async def seed() -> None:
    async with async_session() as session:
        await _clear_demo(session)

        fp = FloorPlan(
            name=DEMO_NAME,
            building=DEMO_BUILDING,
            floor="3",
            svg_url=None,
            image_url=None,
            width=WIDTH,
            height=HEIGHT,
        )
        fp.zones = [Zone(**z) for z in ZONES]
        fp.access_points = [AccessPoint(**ap) for ap in ACCESS_POINTS]
        session.add(fp)
        await session.commit()
        await session.refresh(fp)

        # Column is TIMESTAMP WITHOUT TIME ZONE, so store a naive UTC value.
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        session.add_all(
            Asset(last_floor_id=fp.id, last_seen_at=now, **a) for a in ASSETS
        )
        await session.commit()

        print(
            f"Seeded floor plan {fp.id} "
            f"({fp.building} · {fp.name}) with "
            f"{len(ZONES)} zones, {len(ACCESS_POINTS)} access points, "
            f"{len(ASSETS)} assets."
        )


if __name__ == "__main__":
    asyncio.run(seed())
