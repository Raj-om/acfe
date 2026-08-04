from fastapi import APIRouter
from ..schemas.sensor import SensorSchema, SensorCreate, SensorUpdate
from typing import List

router = APIRouter(tags=["Sensors"])

@router.post("", response_model=SensorSchema)
async def create_sensor(sensor: SensorCreate):
    return SensorSchema(id="sen-1", **sensor.model_dump(), is_active=True)

@router.get("", response_model=List[SensorSchema])
async def list_sensors():
    return []

@router.put("/{id}", response_model=SensorSchema)
async def update_sensor(id: str, sensor: SensorUpdate):
    return SensorSchema(id=id, name="Upd", type="RADAR", location_lat=0.0, location_lon=0.0, reliability_score=1.0, is_active=True, metadata={})
