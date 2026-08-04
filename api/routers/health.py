from fastapi import APIRouter
from ..schemas.common import HealthResponse

router = APIRouter(tags=["Health"])

@router.get("/health", response_model=HealthResponse)
async def get_health():
    return HealthResponse(status="UP", db_connected=True)

@router.get("/metrics")
async def get_metrics():
    return {"requests_per_sec": 100}
