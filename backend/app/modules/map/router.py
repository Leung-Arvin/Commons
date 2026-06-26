from fastapi import APIRouter

router = APIRouter(prefix="/maps", tags=["maps"])

@router.get("/")
async def list_maps():
    return {"maps": []}