from abc import ABC, abstractmethod
from typing import List, Optional, Any
from uuid import UUID
from datetime import datetime
from acfe.core.domain.value_objects import SensorId, SeverityLevel

# Forward references for typing
class Sensor: pass
class FusionResult: pass
class AlertEvent: pass

class ISensorRepository(ABC):
    """Abstract repository for accessing Sensor entities."""
    
    @abstractmethod
    def get_by_id(self, sensor_id: SensorId) -> Optional[Sensor]:
        """Retrieve a sensor by its ID."""
        pass
        
    @abstractmethod
    def get_all(self, active_only: bool = True) -> List[Sensor]:
        """Retrieve all sensors."""
        pass
        
    @abstractmethod
    def create(self, sensor: Sensor) -> Sensor:
        """Create a new sensor in the repository."""
        pass
        
    @abstractmethod
    def update(self, sensor: Sensor) -> Sensor:
        """Update an existing sensor."""
        pass
        
    @abstractmethod
    def delete(self, sensor_id: SensorId) -> bool:
        """Delete a sensor by ID. Returns True if successful."""
        pass
        
    @abstractmethod
    def get_by_reliability_below(self, threshold: float) -> List[Sensor]:
        """Retrieve all sensors with reliability below the specified threshold."""
        pass

class IFusionResultRepository(ABC):
    """Abstract repository for storing and retrieving Fusion Results."""
    
    @abstractmethod
    def get_by_id(self, result_id: UUID) -> Optional[FusionResult]:
        """Retrieve a fusion result by its UUID."""
        pass
        
    @abstractmethod
    def get_by_session(self, session_id: str) -> List[FusionResult]:
        """Retrieve all fusion results for a given session."""
        pass
        
    @abstractmethod
    def save(self, result: FusionResult) -> FusionResult:
        """Save a new fusion result."""
        pass
        
    @abstractmethod
    def get_recent(self, limit: int, since: datetime) -> List[FusionResult]:
        """Retrieve recent fusion results."""
        pass

class IAlertRepository(ABC):
    """Abstract repository for managing Alerts."""
    
    @abstractmethod
    def create(self, alert: AlertEvent) -> AlertEvent:
        """Store a new alert."""
        pass
        
    @abstractmethod
    def get_unacknowledged(self) -> List[AlertEvent]:
        """Retrieve all unacknowledged alerts."""
        pass
        
    @abstractmethod
    def acknowledge(self, alert_id: UUID, user_id: str) -> bool:
        """Mark an alert as acknowledged."""
        pass
        
    @abstractmethod
    def get_by_severity(self, severity: SeverityLevel) -> List[AlertEvent]:
        """Retrieve alerts matching a specific severity level."""
        pass
