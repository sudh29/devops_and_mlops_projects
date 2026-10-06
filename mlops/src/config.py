"""Configuration settings for MLOps pipeline."""
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Predictive Maintenance MLOps"
    VERSION: str = "1.0.0"

    # Base Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"

    # Data files
    RAW_DATA_PATH: Path = DATA_DIR / "sensor_data.csv"
    MODEL_ARTIFACT_PATH: Path = MODELS_DIR / "model_pipeline.joblib"

    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME: str = "predictive-maintenance-experiment"

    # Model Hyperparameters
    N_ESTIMATORS: int = 100
    MAX_DEPTH: int = 6
    RANDOM_STATE: int = 42

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
