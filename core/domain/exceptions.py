class ACFEException(Exception):
    """Base exception for all ACFE related errors."""
    pass

class SensorDataInvalidError(ACFEException):
    """Raised when incoming sensor data is invalid."""
    pass

class FusionComputationError(ACFEException):
    """Raised when a fusion engine fails to compute a result."""
    pass

class CalibrationError(ACFEException):
    """Raised when probability calibration fails."""
    pass

class ConfigurationError(ACFEException):
    """Raised when there is a configuration error."""
    pass
