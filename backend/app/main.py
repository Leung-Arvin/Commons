from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.config import settings
from app.modules.map.router import router as map_router
from app.modules.location.router import router as location_router
from app.modules.location.router import router as ws_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: could init DB pools, Kafka consumers, etc.
    yield
    # Shutdown: cleanup

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(map_router, prefix="/api/v1")
app.include_router(location_router, prefix="/api/v1")
app.include_router(ws_router, prefix="/api/v1")  

@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}