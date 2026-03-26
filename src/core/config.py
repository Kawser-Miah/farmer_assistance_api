"""Application configuration settings.

Manages paths, constants, and environment variables.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path


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
    crop_disease_detection_model_path: Path = base_dir / "assets" / "crop_disease_detection_ml_model.h5"
    crop_disease_detection_class_names_path: Path = base_dir / "assets" / "crop_disease_detection_class_names.json"
    smart_irrigation_model_path: Path = base_dir / "assets" / "best_irrigation_model.pkl"
    fertilizer_model_path: Path = base_dir / "assets" / "fertilizer_model.pkl"
    fertilizer_encoder_path: Path = base_dir / "assets" / "fertilizer_encoder.pkl"
    crop_encoder_path: Path = base_dir / "assets" / "crop_encoder.pkl"
    soil_encoder_path: Path = base_dir / "assets" / "soil_encoder.pkl"
    
    # Aliases for easier access
    model_path: Path = crop_disease_detection_model_path
    class_names_path: Path = crop_disease_detection_class_names_path
    
    # Model Configuration
    prediction_threshold: float = 0.5  # Not currently used, but available
    
    # API Configuration
    crop_disease_detection_prefix: str = "/crop-disease"
    ai_chat_prefix: str = "/ai-chat"
    smart_irrigation_prefix: str = "/smart-irrigation"
    fertilizer_tips_prefix: str = "/fertilizer-tips"
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list = ["*"]  # Change in production
    
    # Supabase Configuration
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_key: str = ""
    google_api_key: str = ""
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )


# Singleton instance
settings = Settings()