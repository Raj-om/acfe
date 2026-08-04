from typing import Dict
from acfe.config.settings import settings

class ReliabilityTracker:
    """
    Track historical accuracy per sensor.
    Exponential moving average reliability score.
    Flag unreliable sensors automatically.
    Detect sensor failure patterns.
    """
    def __init__(self):
        self.sensor_reliabilities: Dict[str, float] = {}
        self.decay_rate = settings.reliability_decay_rate
        self.failure_threshold = 0.3
        
    def update_reliability(self, sensor_id: str, is_correct: bool, confidence: float) -> None:
        """
        Update the EMA reliability score for a sensor.
        Penalize heavily for high confidence but incorrect.
        Reward for high confidence and correct.
        """
        current_rel = self.sensor_reliabilities.get(sensor_id, 0.5)
        
        # Calculate instant score based on correctness and confidence
        if is_correct:
            instant_score = 0.5 + (0.5 * confidence) # [0.5, 1.0]
        else:
            instant_score = 0.5 - (0.5 * confidence) # [0.0, 0.5]
            
        # EMA update
        new_rel = self.decay_rate * current_rel + (1 - self.decay_rate) * instant_score
        
        # Bound
        self.sensor_reliabilities[sensor_id] = max(0.0, min(1.0, new_rel))
        
    def get_reliability(self, sensor_id: str) -> float:
        return self.sensor_reliabilities.get(sensor_id, 0.5)
        
    def is_reliable(self, sensor_id: str) -> bool:
        """Flag unreliable sensors."""
        return self.get_reliability(sensor_id) >= self.failure_threshold
        
    def detect_failure(self, sensor_id: str) -> bool:
        """Detect sensor failure patterns (e.g. constant 0.0 reliability)."""
        rel = self.get_reliability(sensor_id)
        if rel < 0.1:
            return True
        return False
