import numpy as np

class KalmanConfidenceTracker:
    """
    1D Kalman filter for confidence tracking over time.
    State: [confidence, confidence_rate]
    Adaptive noise estimation (Q, R updated via ML-II)
    """
    
    def __init__(self, initial_confidence: float = 0.5):
        # State vector [x, x']
        self.x = np.array([initial_confidence, 0.0])
        # Covariance matrix
        self.P = np.array([[0.1, 0.0],
                           [0.0, 0.1]])
        
        # State transition model
        self.F = np.array([[1.0, 1.0],
                           [0.0, 1.0]])
        
        # Observation model
        self.H = np.array([[1.0, 0.0]])
        
        # Process noise covariance (Adaptive)
        self.Q = np.array([[1e-4, 0.0],
                           [0.0, 1e-4]])
        
        # Measurement noise covariance (Adaptive)
        self.R = np.array([[1e-2]])
        
        self.last_innovation = 0.0
        
    def predict(self, dt: float = 1.0) -> float:
        """Predict the next state."""
        self.F[0, 1] = dt
        self.x = self.F @ self.x
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        # Bound confidence
        self.x[0] = max(0.0, min(1.0, self.x[0]))
        return float(self.x[0])
        
    def update(self, measurement: float) -> None:
        """Update the state with a new measurement."""
        z = np.array([measurement])
        
        # Innovation
        y = z - (self.H @ self.x)
        self.last_innovation = y[0]
        
        # Innovation covariance
        S = self.H @ self.P @ self.H.T + self.R
        
        # Kalman Gain
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # State update
        self.x = self.x + K @ y
        
        # Covariance update
        I = np.eye(2)
        self.P = (I - K @ self.H) @ self.P
        
        # Adaptive noise (ML-II approximation)
        alpha = 0.1
        self.R[0, 0] = (1 - alpha) * self.R[0, 0] + alpha * (y[0] ** 2)
        
        # Bound confidence
        self.x[0] = max(0.0, min(1.0, self.x[0]))
