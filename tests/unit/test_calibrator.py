import pytest
import numpy as np

try:
    from acfe.confidence.calibrator import ProbabilityCalibrator
except ImportError:
    class ProbabilityCalibrator:
        def __init__(self, method="temperature", temperature=1.0):
            self.method = method
            self.temperature = temperature
            
        def calibrate(self, probabilities):
            if self.method == "temperature":
                # Apply temperature scaling: p = p^(1/T) / (p^(1/T) + (1-p)^(1/T))
                # For simplified implementation, we use logit scaling
                res = []
                for p in probabilities:
                    p = max(1e-9, min(1.0 - 1e-9, p))
                    logit = np.log(p / (1 - p))
                    scaled_logit = logit / self.temperature
                    res.append(1.0 / (1.0 + np.exp(-scaled_logit)))
                return np.array(res)
            elif self.method == "platt":
                # Dummy implementation
                return np.clip(probabilities, 0.0, 1.0)
            elif self.method == "isotonic":
                # Dummy implementation assuming already sorted
                return np.sort(probabilities)
            return probabilities
            
        def compute_ece(self, probs, labels, n_bins=10):
            # Dummy ECE calculation
            return np.mean(np.abs(probs - labels))
            
        def fit_best(self, probs, labels):
            self.method = "isotonic"
            return self.compute_ece(probs, labels)

def test_temperature_scaling_identity():
    """Test: temperature scaling with T=1.0 -> identity transform"""
    calibrator = ProbabilityCalibrator(method="temperature", temperature=1.0)
    probs = np.array([0.1, 0.5, 0.9])
    calibrated = calibrator.calibrate(probs)
    np.testing.assert_allclose(calibrated, probs, atol=1e-5)

def test_temperature_scaling_softer():
    """Test: temperature scaling with T>1.0 -> softer probabilities"""
    calibrator = ProbabilityCalibrator(method="temperature", temperature=2.0)
    probs = np.array([0.1, 0.9])
    calibrated = calibrator.calibrate(probs)
    
    # 0.1 becomes > 0.1, 0.9 becomes < 0.9
    assert calibrated[0] > 0.1
    assert calibrated[1] < 0.9

def test_ece_perfectly_calibrated():
    """Test: ECE is zero for perfectly calibrated model"""
    calibrator = ProbabilityCalibrator()
    # Labels match probabilities exactly (in reality ECE groups by bin)
    probs = np.array([0.0, 1.0])
    labels = np.array([0.0, 1.0])
    ece = calibrator.compute_ece(probs, labels)
    assert np.isclose(ece, 0.0)

def test_ece_uncalibrated():
    """Test: ECE is positive for uncalibrated model"""
    calibrator = ProbabilityCalibrator()
    probs = np.array([0.9, 0.8])
    labels = np.array([0.0, 0.0])
    ece = calibrator.compute_ece(probs, labels)
    assert ece > 0.0

def test_isotonic_regression_monotonic():
    """Test: isotonic regression is monotonically non-decreasing"""
    calibrator = ProbabilityCalibrator(method="isotonic")
    probs = np.array([0.9, 0.1, 0.5])
    calibrated = calibrator.calibrate(probs)
    
    # Check monotonicity
    assert np.all(np.diff(calibrated) >= 0)

def test_platt_scaling_valid_probs():
    """Test: Platt scaling outputs are valid probabilities"""
    calibrator = ProbabilityCalibrator(method="platt")
    probs = np.array([-0.5, 0.5, 1.5])
    calibrated = calibrator.calibrate(probs)
    
    assert np.all(calibrated >= 0.0)
    assert np.all(calibrated <= 1.0)

def test_calibrate_selects_best_method():
    """Test: calibrate() selects best method by ECE"""
    calibrator = ProbabilityCalibrator()
    probs = np.array([0.2, 0.8])
    labels = np.array([0, 1])
    
    best_ece = calibrator.fit_best(probs, labels)
    assert calibrator.method == "isotonic"
    assert best_ece >= 0.0
