from dataclasses import dataclass
from enum import Enum
from typing import Optional
import re

@dataclass(frozen=True)
class Confidence:
    """Represents a confidence score in [0, 1]."""
    value: float
    
    def __post_init__(self):
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"Confidence value {self.value} must be between 0.0 and 1.0")

@dataclass(frozen=True)
class Uncertainty:
    """Represents the uncertainty associated with a measurement."""
    aleatoric: float
    epistemic: float
    
    def __post_init__(self):
        if self.aleatoric < 0.0 or self.epistemic < 0.0:
            raise ValueError("Uncertainty components must be non-negative")
            
    @property
    def total(self) -> float:
        """Calculate total uncertainty (e.g., sum or quadrature)."""
        return self.aleatoric + self.epistemic

@dataclass(frozen=True)
class Weight:
    """Represents a weight for fusion algorithms in [0, 1]."""
    value: float
    
    def __post_init__(self):
        if not (0.0 <= self.value <= 1.0):
            raise ValueError(f"Weight value {self.value} must be between 0.0 and 1.0")

@dataclass(frozen=True)
class SensorId:
    """Represents a unique, valid sensor identifier."""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Sensor ID cannot be empty")
        if not re.match(r'^[a-zA-Z0-9_]+$', self.value):
            raise ValueError("Sensor ID must be alphanumeric and underscores only")

@dataclass(frozen=True)
class Location:
    """Represents geographic coordinates."""
    lat: float
    lon: float
    alt: Optional[float] = None
    
    def __post_init__(self):
        if not (-90.0 <= self.lat <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180.0 <= self.lon <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")

class SeverityLevel(Enum):
    """Severity levels for alerts."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class FusionMethod(Enum):
    """Supported fusion methodologies."""
    BAYESIAN = "BAYESIAN"
    DEMPSTER_SHAFER = "DEMPSTER_SHAFER"
    KALMAN = "KALMAN"
    ACFE_CORE = "ACFE_CORE"
    ACFE_TEMPORAL = "ACFE_TEMPORAL"
    ACFE_GRAPH = "ACFE_GRAPH"
    ACFE_FULL = "ACFE_FULL"

class SensorType(Enum):
    """Supported sensor types."""
    CAMERA = "CAMERA"
    LIDAR = "LIDAR"
    RADAR = "RADAR"
    WEATHER = "WEATHER"
    SEISMIC = "SEISMIC"
    SATELLITE = "SATELLITE"
    IOT = "IOT"
    SCADA = "SCADA"
    NETWORK = "NETWORK"
    TEXT = "TEXT"
