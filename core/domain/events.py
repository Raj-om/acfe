from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Dict
from uuid import UUID, uuid4

@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events."""
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass(frozen=True)
class FusionCompletedEvent(DomainEvent):
    """Event emitted when a fusion operation completes."""
    fusion_id: UUID
    fused_confidence: float
    method: str
    source_count: int
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not (0.0 <= self.fused_confidence <= 1.0):
            raise ValueError("fused_confidence must be between 0.0 and 1.0")
        if self.source_count < 0:
            raise ValueError("source_count cannot be negative")

@dataclass(frozen=True)
class AlertGeneratedEvent(DomainEvent):
    """Event emitted when an alert is generated based on fusion results."""
    alert_id: UUID
    severity: str
    confidence: float
    location: Optional[Dict[str, float]]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be between 0.0 and 1.0")

@dataclass(frozen=True)
class SensorDegradedEvent(DomainEvent):
    """Event emitted when a sensor's reliability degrades below a threshold."""
    sensor_id: str
    old_reliability: float
    new_reliability: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not (0.0 <= self.old_reliability <= 1.0) or not (0.0 <= self.new_reliability <= 1.0):
            raise ValueError("reliability scores must be between 0.0 and 1.0")

@dataclass(frozen=True)
class SensorFailedEvent(DomainEvent):
    """Event emitted when a sensor completely fails or disconnects."""
    sensor_id: str
    failure_reason: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass(frozen=True)
class ReliabilityUpdatedEvent(DomainEvent):
    """Event emitted when a sensor's reliability score is updated."""
    sensor_id: str
    new_reliability: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not (0.0 <= self.new_reliability <= 1.0):
            raise ValueError("reliability must be between 0.0 and 1.0")

@dataclass(frozen=True)
class CalibrationAppliedEvent(DomainEvent):
    """Event emitted when probability calibration is applied to confidence scores."""
    method: str
    before_ece: float
    after_ece: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        if self.before_ece < 0 or self.after_ece < 0:
            raise ValueError("ECE must be non-negative")
