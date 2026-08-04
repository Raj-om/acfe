from fastapi import APIRouter
from ..schemas.alert import AlertSchema, AlertCreate
from typing import List

router = APIRouter(tags=["Alerts"])

@router.get("", response_model=List[AlertSchema])
async def list_alerts():
    return []

@router.post("/ack")
async def acknowledge_alert(alert_id: str):
    return {"status": "acknowledged"}
