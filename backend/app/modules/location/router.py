from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.location.models import AssetCreate, AssetRead, AssetUpdate, LocateRequest
from app.modules.location import service
from app.modules.location.websocket_manager import manager

# HTTP endpoints under /assets
router = APIRouter(prefix="/assets", tags=["assets"])

@router.get("/", response_model=list[AssetRead])
async def list_assets(db: AsyncSession = Depends(get_db)):
    return await service.list_assets(db)

@router.post("/", response_model=AssetRead, status_code=201)
async def create_asset(data: AssetCreate, db: AsyncSession = Depends(get_db)):
    return await service.create_asset(db, data)

@router.get("/{asset_id}", response_model=AssetRead)
async def get_asset(asset_id: UUID, db: AsyncSession = Depends(get_db)):
    asset = await service.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.put("/{asset_id}", response_model=AssetRead)
async def update_asset(asset_id: UUID, data: AssetUpdate, db: AsyncSession = Depends(get_db)):
    asset = await service.update_asset(db, asset_id, data)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.delete("/{asset_id}", status_code=204)
async def delete_asset(asset_id: UUID, db: AsyncSession = Depends(get_db)):
    if not await service.delete_asset(db, asset_id):
        raise HTTPException(status_code=404, detail="Asset not found")

@router.post("/{asset_id}/locate", response_model=AssetRead)
async def locate_asset(asset_id: UUID, data: LocateRequest, db: AsyncSession = Depends(get_db)):
    asset = await service.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    updated = await service.record_asset_location(db, asset, data.floor_plan_id, data.readings)
    if updated is None:
        raise HTTPException(
            status_code=422, detail="Insufficient AP readings to compute a position"
        )
    return updated

# WebSocket endpoint at root level (not under /assets)
ws_router = APIRouter(tags=["websocket"])

@ws_router.websocket("/ws/locations")
async def websocket_locations(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)