from typing import Dict, List, Optional
from acfe.core.domain.entities import SensorReading, ConfidenceScore, FusionResult
from acfe.fusion.acfe_core import ACFECoreEngine
from acfe.confidence.reliability import ReliabilityTracker
from acfe.confidence.calibrator import ProbabilityCalibrator
from datetime import datetime

class FuseObservationsUseCase:
    """
    Main use case for fusing observations from multiple sensors.
    Applies the ACFE Core Engine and uses reliability tracking and calibration.
    """
    def __init__(
        self, 
        fusion_engine: ACFECoreEngine,
        reliability_tracker: ReliabilityTracker,
        calibrator: ProbabilityCalibrator
    ):
        self.fusion_engine = fusion_engine
        self.reliability_tracker = reliability_tracker
        self.calibrator = calibrator

    def execute(self, readings: List[SensorReading], current_time: Optional[datetime] = None) -> FusionResult:
        if not readings:
            raise ValueError("No readings to fuse")
            
        current_time = current_time or datetime.utcnow()
        
        # 1. Process readings into confidence scores and metadata
        scores: Dict[str, ConfidenceScore] = {}
        reliabilities: Dict[str, float] = {}
        recency_decays: Dict[str, float] = {}
        
        for r in readings:
            # Assuming value [0, 1] is raw confidence
            # In a real scenario, map raw values to confidence
            raw_conf = r.value
            
            scores[r.sensor_id] = ConfidenceScore(
                score=raw_conf,
                uncertainty=1.0 - raw_conf,  # Simplified uncertainty
                calibrated=False,
                source=r.source_type
            )
            
            # Fetch reliability
            reliabilities[r.sensor_id] = self.reliability_tracker.get_reliability(r.sensor_id)
            
            # Compute recency decay
            time_diff = (current_time - r.timestamp).total_seconds()
            # simple exponential decay
            decay = max(0.01, min(1.0, 1.0 / (1.0 + time_diff * 0.1)))
            recency_decays[r.sensor_id] = decay
            
        # 2. Perform Fusion
        fusion_result = self.fusion_engine.fuse(
            scores=scores,
            reliabilities=reliabilities,
            recency_decays=recency_decays
        )
        
        return fusion_result
