from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ObservationSchema(BaseModel):
    sensor_id: str
    confidence: float
    timestamp: datetime
    data: Dict[str, Any]

class FusionRequest(BaseModel):
    session_id: str
    observations: List[ObservationSchema]

class FusionResponse(BaseModel):
    id: str
    session_id: str
    fused_confidence: float
    uncertainty: float
    conflict_level: float
    method_used: str
    sources: List[str]
    weights: Dict[str, float]
    explanation: Dict[str, Any]
