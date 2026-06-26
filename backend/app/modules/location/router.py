from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.location.models import AssetCreate, AssetRead
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