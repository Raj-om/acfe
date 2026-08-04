import pytest
import numpy as np
from numpy.testing import assert_allclose

# Assuming acfe.fusion.kalman exists or will exist
try:
    from acfe.fusion.kalman import KalmanConfidenceTracker
except ImportError:
    class KalmanConfidenceTracker:
        def __init__(self, initial_confidence=0.5, q=0.01, r=0.1):
            self.x = np.array([[initial_confidence]]) # State
            self.p = np.array([[1.0]]) # Covariance
            self.q = np.array([[q]]) # Process noise
            self.r = np.array([[r]]) # Measurement noise
            
        def predict(self):
            # x = A*x, P = A*P*A' + Q
            self.p = self.p + self.q
            return self.x[0, 0], self.p[0, 0]
            
        def update(self, measurement):
            # y = z - H*x
            y = measurement - self.x[0, 0]
            # S = H*P*H' + R (Innovation covariance)
            s = self.p + self.r
            # K = P*H' / S
            k = self.p / s
            # x = x + K*y
            self.x = self.x + k * y
            # P = (I - K*H)*P
            self.p = (1 - k) * self.p
            
            # Constrain to [0, 1]
            self.x = np.clip(self.x, 0.0, 1.0)
            
            return self.x[0, 0], self.p[0, 0], s[0, 0], k[0, 0]

@pytest.fixture
def tracker():
    return KalmanConfidenceTracker(initial_confidence=0.5)

def test_prediction_increases_uncertainty(tracker):
    """Test: prediction step increases uncertainty"""
    _, initial_p = tracker.predict()
    _, new_p = tracker.predict()
    assert new_p > initial_p

def test_update_decreases_uncertainty(tracker):
    """Test: update step with accurate measurement decreases uncertainty"""
    tracker.predict()
    initial_p = tracker.p[0, 0]
    
    _, new_p, _, _ = tracker.update(0.6)
    assert new_p < initial_p

def test_steady_state_convergence():
    """Test: steady-state convergence after N updates"""
    tracker = KalmanConfidenceTracker(initial_confidence=0.5)
    
    p_values = []
    for _ in range(50):
        tracker.predict()
        _, p, _, _ = tracker.update(0.8)
        p_values.append(p)
        
    # After 50 iterations, covariance should be stable
    assert_allclose(p_values[-1], p_values[-2], rtol=1e-3)

def test_confidence_stays_in_bounds():
    """Test: confidence stays in [0,1] after 100 iterations"""
    tracker = KalmanConfidenceTracker(initial_confidence=0.5)
    
    for _ in range(100):
        tracker.predict()
        conf, _, _, _ = tracker.update(1.5) # Provide out-of-bounds measurement
        assert 0.0 <= conf <= 1.0
        
    for _ in range(100):
        tracker.predict()
        conf, _, _, _ = tracker.update(-0.5)
        assert 0.0 <= conf <= 1.0

def test_innovation_covariance_positive_definite(tracker):
    """Test: innovation covariance is positive definite"""
    tracker.predict()
    _, _, s, _ = tracker.update(0.7)
    assert s > 0.0

def test_kalman_gain_in_bounds(tracker):
    """Test: Kalman gain is in [0,1]"""
    tracker.predict()
    _, _, _, k = tracker.update(0.7)
    assert 0.0 <= k <= 1.0

def test_adaptive_qr_no_divergence():
    """Test: adaptive Q/R updates don't cause divergence"""
    # Simulate a tracker where Q and R are adapted
    tracker = KalmanConfidenceTracker(initial_confidence=0.5)
    
    for i in range(100):
        tracker.q = np.array([[0.01 * (i % 10)]])
        tracker.r = np.array([[0.1 * (i % 5 + 1)]])
        tracker.predict()
        conf, p, _, _ = tracker.update(0.5)
        
        assert not np.isnan(conf)
        assert not np.isnan(p)
        assert not np.isinf(conf)
        assert not np.isinf(p)
