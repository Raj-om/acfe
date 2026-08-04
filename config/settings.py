from pydantic import BaseSettings

class ACFEConfig(BaseSettings):
    """Application configuration for the ACFE project."""
    environment: str = "production"
    debug: bool = False
    
    # Fusion thresholds
    yager_conflict_threshold: float = 0.3
    
    # Kalman filter params
    kalman_process_noise: float = 1e-4
    kalman_measurement_noise: float = 1e-2
    
    # Reliability tracking
    reliability_decay_rate: float = 0.95
    
    # Model paths
    gnn_model_path: str = "models/acfe_graph_v1.pt"
    
    class Config:
        env_prefix = "ACFE_"
        env_file = ".env"

settings = ACFEConfig()
