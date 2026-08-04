from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
from acfe.core.domain.value_objects import SensorId, Confidence

# Forward references for typing
class SensorReading: pass
class FusionResult: pass
class ConfidenceScore: pass
class ExplanationReport: pass

class IFusionEngine(ABC):
    """Abstract interface for a data fusion engine."""
    
    @abstractmethod
    def fuse(self, readings: List[SensorReading]) -> FusionResult:
        """Perform fusion on a list of sensor readings."""
        pass
        
    @abstractmethod
    def get_method_name(self) -> str:
        """Get the name of the fusion method used."""
        pass
        
    @abstractmethod
    def supports_explainability(self) -> bool:
        """Check if this fusion engine supports generating explanations."""
        pass

class IConfidenceEstimator(ABC):
    """Abstract interface for estimating confidence scores."""
    
    @abstractmethod
    def estimate(self, reading: SensorReading) -> ConfidenceScore:
        """Estimate the confidence score for a given reading."""
        pass
        
    @abstractmethod
    def calibrate(self, scores: List[ConfidenceScore], labels: List[int]) -> None:
        """Calibrate the confidence estimator using historical data and labels."""
        pass

class IReliabilityTracker(ABC):
    """Abstract interface for tracking sensor reliability over time."""
    
    @abstractmethod
    def get_reliability(self, sensor_id: SensorId) -> float:
        """Get the current reliability score for a sensor."""
        pass
        
    @abstractmethod
    def update(self, sensor_id: SensorId, correct: bool) -> None:
        """Update the reliability score for a sensor based on an outcome."""
        pass
        
    @abstractmethod
    def flag_unreliable(self, sensor_id: SensorId) -> None:
        """Manually flag a sensor as unreliable."""
        pass

class IExplainer(ABC):
    """Abstract interface for explaining fusion results."""
    
    @abstractmethod
    def explain(self, result: FusionResult) -> ExplanationReport:
        """Generate an explanation report for a fusion result."""
        pass
        
    @abstractmethod
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importance scores from the underlying models."""
        pass

class ICacheService(ABC):
    """Abstract interface for caching operations."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from cache."""
        pass
        
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int) -> None:
        """Set a value in cache with a time-to-live (seconds)."""
        pass
        
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a value from cache."""
        pass

class IEventPublisher(ABC):
    """Abstract interface for publishing domain events."""
    
    @abstractmethod
    def publish(self, event: Any) -> None:
        """Publish a single domain event."""
        pass
        
    @abstractmethod
    def publish_batch(self, events: List[Any]) -> None:
        """Publish multiple domain events."""
        pass
