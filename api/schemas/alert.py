from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertCreate(BaseModel):
    severity: str
    title: str
    description: str
    location_lat: float
    location_lon: float
    confidence: float

class AlertSchema(AlertCreate):
    id: str
    acknowledged: bool
    acknowledged_by: Optional[str] = None
    created_at: datetime
