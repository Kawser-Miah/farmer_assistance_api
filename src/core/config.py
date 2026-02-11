"""Application configuration settings.

Manages paths, constants, and environment variables.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path

print(f"Debug: Base directory is {Path(__file__).parent.parent.parent}")
class Settings(BaseSettings):
    """Application settings and configuration.
    
    Can be overridden by environment variables.
    """
    
    # API Metadata
    app_name: str = "AI-Powered Smart Farming Assistant"
    version: str = "1.0.0"
    description: str = "Machine learning API for Smart Farming Assistant"
    
    # Path Configuration
    base_dir: Path = Path(__file__).parent.parent.parent
    model_path: Path = base_dir / "artifacts" / "heart-disease-prediction-knn-model.pkl"
    scaler_path: Path = base_dir / "artifacts" / "scaler.pkl"
    
    # Model Configuration
    prediction_threshold: float = 0.5  # Not currently used, but available
    
    # API Configuration
    crop_disease_detection_prefix: str = "/crop-disease"
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list = ["*"]  # Change in production
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False
    )


# Singleton instance
settings = Settings()