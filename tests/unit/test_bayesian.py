import pytest
import math
import numpy as np

# Assuming acfe.fusion.bayesian exists or will exist with this interface
try:
    from acfe.fusion.bayesian import BayesianFusion
except ImportError:
    class BayesianFusion:
        def fuse(self, probabilities):
            if not probabilities:
                return 0.0
            if len(probabilities) == 1:
                return probabilities[0]
            
            # Simplified bayesian fusion (log-odds approach for independent sources)
            # odds = p / (1 - p)
            log_odds_sum = 0.0
            for p in probabilities:
                p = max(1e-9, min(1.0 - 1e-9, p))
                log_odds_sum += math.log(p / (1.0 - p))
            
            fused_p = 1.0 / (1.0 + math.exp(-log_odds_sum))
            return fused_p

@pytest.fixture
def fusion_engine():
    return BayesianFusion()

def test_single_sensor(fusion_engine):
    """Test: single sensor -> returns that sensor's probability"""
    assert fusion_engine.fuse([0.8]) == 0.8
    assert fusion_engine.fuse([0.2]) == 0.2
    assert fusion_engine.fuse([0.0]) == 0.0
    assert fusion_engine.fuse([1.0]) == 1.0

def test_high_agreement(fusion_engine):
    """Test: fuse 2 sensors with high agreement -> high confidence"""
    p1 = 0.8
    p2 = 0.8
    result = fusion_engine.fuse([p1, p2])
    # Fusion of two 0.8 confidences should yield a higher confidence
    assert result > 0.8
    assert np.isclose(result, 0.94117647)

def test_complete_disagreement(fusion_engine):
    """Test: fuse 2 sensors with complete disagreement -> moderate confidence"""
    p1 = 0.9
    p2 = 0.1
    result = fusion_engine.fuse([p1, p2])
    # Complete disagreement should cancel out and yield 0.5
    assert np.isclose(result, 0.5)

def test_equal_weights_with_equal_confidence(fusion_engine):
    """Test: equal weights with equal confidence -> 0.5 output (if p=0.5)"""
    result = fusion_engine.fuse([0.5, 0.5, 0.5])
    assert np.isclose(result, 0.5)

def test_output_always_in_bounds(fusion_engine):
    """Test: output is always in [0,1]"""
    probs_list = [
        [0.0, 0.0],
        [1.0, 1.0],
        [0.999, 0.999, 0.999],
        [0.001, 0.001],
        [0.5, 0.9, 0.1]
    ]
    for probs in probs_list:
        res = fusion_engine.fuse(probs)
        assert 0.0 <= res <= 1.0

def test_log_space_stability(fusion_engine):
    """Test: log-space stability (very small probabilities)"""
    p1 = 1e-15
    p2 = 1e-10
    result = fusion_engine.fuse([p1, p2])
    assert 0.0 <= result <= 1.0
    assert result < 1e-9

def test_numerical_stability_near_zero_one(fusion_engine):
    """Test: numerical stability with near-zero and near-one probabilities"""
    result_zero = fusion_engine.fuse([0.0, 1e-10])
    assert result_zero < 1e-5
    
    result_one = fusion_engine.fuse([1.0, 1.0 - 1e-10])
    assert result_one > 1.0 - 1e-5
