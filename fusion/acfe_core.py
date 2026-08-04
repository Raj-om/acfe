import numpy as np
from typing import List, Dict, Tuple
from acfe.core.domain.entities import SensorReading, ConfidenceScore, FusionResult
from acfe.config.settings import settings

class ACFECoreEngine:
    """
    Adaptive Confidence Fusion Engine - Core Algorithm.
    Implements an adaptive Bayesian-Dempster-Shafer hybrid.
    """
    
    def __init__(self, yager_conflict_threshold: float = None):
        self.yager_conflict_threshold = yager_conflict_threshold or settings.yager_conflict_threshold

    def compute_dynamic_weights(self, reliabilities: Dict[str, float], recency_decays: Dict[str, float]) -> Dict[str, float]:
        """
        w_i(t) = reliability_i(t) * recency_decay_i(t) / Z
        """
        unnormalized = {}
        for sensor_id in reliabilities:
            r = reliabilities.get(sensor_id, 0.5)
            d = recency_decays.get(sensor_id, 1.0)
            unnormalized[sensor_id] = r * d
            
        Z = sum(unnormalized.values())
        if Z == 0:
            return {s: 1.0 / len(unnormalized) for s in unnormalized}
        
        return {s: v / Z for s, v in unnormalized.items()}

    def bayesian_fusion(self, scores: Dict[str, ConfidenceScore], weights: Dict[str, float]) -> float:
        """
        Bayesian posterior: P(H|e_1,...,e_N) computed via log-odds accumulation.
        """
        log_odds_sum = 0.0
        for sensor_id, score in scores.items():
            p = score.score
            p = max(1e-5, min(1.0 - 1e-5, p)) # clip
            w = weights.get(sensor_id, 1.0)
            log_odds = np.log(p / (1 - p))
            log_odds_sum += w * log_odds
            
        p_fused = 1.0 / (1.0 + np.exp(-log_odds_sum))
        return p_fused

    def dempster_shafer_fusion(self, scores: Dict[str, ConfidenceScore], weights: Dict[str, float]) -> float:
        """
        DS combination with Yager conflict handling.
        """
        # Mass functions: m({H}) = p * w, m({not H}) = (1-p) * w, m(Omega) = 1 - w
        # For simplicity in this core engine, we compute combined belief.
        # This is a simplified 2-class (H, not H) implementation.
        
        m_H = 1.0
        m_not_H = 1.0
        
        for sensor_id, score in scores.items():
            w = weights.get(sensor_id, 1.0)
            p = score.score
            
            # Simple discounting
            m_H_i = p * w
            m_not_H_i = (1 - p) * w
            m_Omega_i = 1.0 - w
            
            # Update (ignoring exact denominator for brevity)
            m_H *= (m_H_i + m_Omega_i)
            m_not_H *= (m_not_H_i + m_Omega_i)
            
        # Conflict K
        K = 1.0 - (m_H + m_not_H)
        K = max(0.0, min(1.0, K))
        
        if K < 1.0:
            m_H_fused = m_H / (1.0 - K)
        else:
            m_H_fused = 0.0
            
        return m_H_fused

    def compute_conflict(self, scores: Dict[str, ConfidenceScore]) -> float:
        """Estimate the degree of conflict K among the sources."""
        values = [s.score for s in scores.values()]
        if not values:
            return 0.0
        variance = np.var(values)
        # Map variance to conflict [0, 1]
        K = 1.0 - np.exp(-variance * 10)
        return float(K)

    def fuse(self, 
             scores: Dict[str, ConfidenceScore], 
             reliabilities: Dict[str, float],
             recency_decays: Dict[str, float]) -> FusionResult:
        """
        Adaptive switching between Bayesian and DS based on conflict level K.
        If K < 0.3: use Bayesian, If K >= 0.3: use Yager-modified DS.
        """
        if not scores:
            raise ValueError("No scores provided for fusion.")
            
        weights = self.compute_dynamic_weights(reliabilities, recency_decays)
        K = self.compute_conflict(scores)
        
        explanation = {
            "conflict_K": K,
            "weights": weights,
            "method": ""
        }
        
        if K < self.yager_conflict_threshold:
            fused_score = self.bayesian_fusion(scores, weights)
            explanation["method"] = "Bayesian"
        else:
            fused_score = self.dempster_shafer_fusion(scores, weights)
            explanation["method"] = "Dempster-Shafer (Yager)"
            
        return FusionResult(
            fused_confidence=fused_score,
            contributing_sources=list(scores.keys()),
            weights=weights,
            explanation=explanation
        )
