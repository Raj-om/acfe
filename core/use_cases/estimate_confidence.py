import logging
import math
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from acfe.core.domain.value_objects import SensorId, Confidence
from acfe.core.ports.services import IConfidenceEstimator, IReliabilityTracker

logger = logging.getLogger(__name__)

# Dummy classes for types
class SensorReading:
    def __init__(self, sensor_id_str: str, timestamp: datetime, value: Any):
        self.sensor_id = SensorId(sensor_id_str)
        self.timestamp = timestamp
        self.value = value

class ConfidenceScore:
    def __init__(self, value: float, reliability: float = 1.0, is_calibrated: bool = False):
        self.confidence = Confidence(value)
        self.reliability = reliability
        self.is_calibrated = is_calibrated

class EstimateConfidenceUseCase:
    """Use case to estimate the confidence of a sensor reading."""
    
    def __init__(self, 
                 estimator: IConfidenceEstimator, 
                 reliability_tracker: IReliabilityTracker,
                 max_age_seconds: int = 300,
                 decay_rate: float = 0.05):
        self.estimator = estimator
        self.reliability_tracker = reliability_tracker
        self.max_age_seconds = max_age_seconds
        self.decay_rate = decay_rate
        
    def execute(self, reading: SensorReading, context: Optional[Dict[str, Any]] = None) -> ConfidenceScore:
        """
        Executes the confidence estimation workflow.
        
        Steps:
        1. Validate reading
        2. Get sensor reliability
        3. Call IConfidenceEstimator.estimate
        4. Apply temporal decay
        5. Return populated ConfidenceScore
        """
        logger.info(f"Estimating confidence for sensor {reading.sensor_id.value}")
        
        # 1. Validate reading
        if not reading:
            raise ValueError("Reading cannot be null")
            
        now = datetime.now(timezone.utc)
        age = (now - reading.timestamp).total_seconds()
        
        if age > self.max_age_seconds:
            logger.warning(f"Reading from sensor {reading.sensor_id.value} is stale (age: {age}s)")
            raise ValueError(f"Reading is too old (> {self.max_age_seconds}s)")
            
        if age < 0:
            logger.warning(f"Reading from sensor {reading.sensor_id.value} has a future timestamp")
            age = 0
            
        # 2. Get sensor reliability
        try:
            reliability = self.reliability_tracker.get_reliability(reading.sensor_id)
        except Exception as e:
            logger.error(f"Failed to get reliability for sensor {reading.sensor_id.value}: {e}")
            reliability = 0.5 # fallback
            
        # 3. Call estimator
        base_score = self.estimator.estimate(reading)
        
        # 4. Apply temporal decay (exponential decay based on age)
        # score = base_score * exp(-decay_rate * (age / 60))
        age_minutes = age / 60.0
        decay_factor = math.exp(-self.decay_rate * age_minutes)
        
        final_value = base_score.confidence.value * decay_factor
        final_value = max(0.0, min(1.0, final_value))
        
        # We assume calibration is handled inside the estimator or can be added here
        
        logger.debug(f"Confidence estimated: base={base_score.confidence.value}, "
                     f"decayed={final_value}, reliability={reliability}")
                     
        return ConfidenceScore(value=final_value, reliability=reliability, is_calibrated=True)
