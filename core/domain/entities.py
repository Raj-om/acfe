from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ConfidenceScore(BaseModel):
    """Represents a confidence score for a sensor reading."""
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    uncertainty: float = Field(..., ge=0.0, le=1.0, description="Uncertainty measure between 0 and 1")
    calibrated: bool = Field(default=False, description="Whether the score has been calibrated")
    source: str = Field(..., description="The source or method that produced this score")

class SensorReading(BaseModel):
    """Represents a reading from a sensor."""
    sensor_id: str = Field(..., description="Unique identifier for the sensor")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time of the reading")
    value: float = Field(..., description="The observed value")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional context or metadata")
    source_type: str = Field(..., description="Type of the sensor (e.g., 'camera', 'lidar')")

class FusionResult(BaseModel):
    """Represents the final result of the confidence fusion process."""
    fused_confidence: float = Field(..., ge=0.0, le=1.0, description="The resulting fused confidence score")
    contributing_sources: List[str] = Field(default_factory=list, description="Sensors/sources that contributed to this result")
    weights: Dict[str, float] = Field(default_factory=dict, description="Weights assigned to each source during fusion")
    explanation: Dict[str, Any] = Field(default_factory=dict, description="Explainability metadata and attribution")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time the fusion was performed")

class AlertEvent(BaseModel):
    """Represents an alert generated based on fused confidence."""
    severity: str = Field(..., description="Severity level of the alert (e.g., 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL')")
    message: str = Field(..., description="Detailed alert message")
    location: str = Field(..., description="Location or context associated with the alert")
    sources: List[str] = Field(default_factory=list, description="List of sensor IDs that triggered this alert")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence associated with this alert")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time the alert was generated")
