import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.linear_model import LogisticRegression

class ProbabilityCalibrator:
    """
    Probability Calibrator for confidence scores.
    Implements TemperatureScaling, IsotonicRegression, PlattScaling.
    Computes ECE (Expected Calibration Error).
    """
    def __init__(self):
        self.iso_reg = IsotonicRegression(out_of_bounds='clip')
        self.platt = LogisticRegression()
        self.temperature = 1.0
        self.method = "isotonic"
        
    def fit(self, y_true: np.ndarray, y_prob: np.ndarray):
        """Fit calibration models and select the best one based on ECE."""
        # Fit Isotonic
        self.iso_reg.fit(y_prob, y_true)
        
        # Fit Platt Scaling (Logistic Regression on scores)
        self.platt.fit(y_prob.reshape(-1, 1), y_true)
        
        # Fit Temperature Scaling (simplified, just search scalar)
        best_t = 1.0
        best_ece = float('inf')
        for t in [0.5, 0.8, 1.0, 1.5, 2.0, 2.5]:
            calib = y_prob ** (1/t) / (y_prob ** (1/t) + (1-y_prob) ** (1/t))
            ece = self.compute_ece(y_true, calib)
            if ece < best_ece:
                best_ece = ece
                best_t = t
        self.temperature = best_t
        
        # Compare ECEs
        iso_calib = self.iso_reg.predict(y_prob)
        platt_calib = self.platt.predict_proba(y_prob.reshape(-1, 1))[:, 1]
        
        ece_iso = self.compute_ece(y_true, iso_calib)
        ece_platt = self.compute_ece(y_true, platt_calib)
        ece_temp = best_ece
        
        best_overall = min(ece_iso, ece_platt, ece_temp)
        if best_overall == ece_iso:
            self.method = "isotonic"
        elif best_overall == ece_platt:
            self.method = "platt"
        else:
            self.method = "temperature"
            
    def calibrate(self, y_prob: np.ndarray) -> np.ndarray:
        """Calibrate probabilities using the best fitted method."""
        if self.method == "isotonic":
            return self.iso_reg.predict(y_prob)
        elif self.method == "platt":
            return self.platt.predict_proba(y_prob.reshape(-1, 1))[:, 1]
        else:
            return y_prob ** (1/self.temperature) / (y_prob ** (1/self.temperature) + (1-y_prob) ** (1/self.temperature))

    @staticmethod
    def compute_ece(y_true: np.ndarray, y_prob: np.ndarray, n_bins: int = 10) -> float:
        """Compute Expected Calibration Error."""
        bins = np.linspace(0.0, 1.0, n_bins + 1)
        binids = np.digitize(y_prob, bins) - 1
        
        ece = 0.0
        for i in range(n_bins):
            mask = binids == i
            if np.any(mask):
                acc = np.mean(y_true[mask])
                conf = np.mean(y_prob[mask])
                weight = np.sum(mask) / len(y_prob)
                ece += weight * np.abs(acc - conf)
        return float(ece)
