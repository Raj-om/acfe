from fastapi import APIRouter

router = APIRouter(tags=["Admin"])

@router.post("/config")
async def update_config(config: dict):
    return {"status": "updated"}
