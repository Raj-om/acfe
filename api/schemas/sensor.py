from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class SensorBase(BaseModel):
    name: str
    type: str
    location_lat: float
    location_lon: float
    reliability_score: float
    metadata: Dict[str, Any]

class SensorCreate(SensorBase):
    pass

class SensorUpdate(BaseModel):
    reliability_score: Optional[float] = None
    is_active: Optional[bool] = None

class SensorSchema(SensorBase):
    id: str
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
