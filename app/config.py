import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file from backend directory or project root
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
root_dir = os.path.abspath(os.path.join(backend_dir, ".."))
load_dotenv(os.path.join(backend_dir, ".env"))
load_dotenv(os.path.join(root_dir, ".env"))

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    PROJECT_NAME: str = "QualiVision AI API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    BASE_DIR: str = backend_dir
    
    DATA_ROOT: str = ""
    DATABASE_URL: str = ""
    UPLOAD_DIR: str = ""
    HEATMAP_DIR: str = ""
    SAMPLES_DIR: str = ""
    
    MAX_UPLOAD_SIZE_MB: int = 15
    CORS_ORIGINS: str = "*"
    SECRET_KEY: str = "qualivision-ai-secret-key-change-in-production"

    def model_post_init(self, __context):
        is_serverless = bool(
            os.environ.get("VERCEL")
            or os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
            or os.environ.get("LAMBDA_TASK_ROOT")
        )
        if is_serverless:
            self.DATA_ROOT = "/tmp"
            self.DATABASE_URL = "sqlite:////tmp/qualivision.db"
            self.UPLOAD_DIR = "/tmp/uploads"
            self.HEATMAP_DIR = "/tmp/heatmaps"
            self.SAMPLES_DIR = "/tmp/samples"
        else:
            if not self.DATA_ROOT or self.DATA_ROOT == "./data":
                self.DATA_ROOT = os.path.join(self.BASE_DIR, "data")
            if not self.DATABASE_URL or "sqlite:///./data" in self.DATABASE_URL:
                self.DATABASE_URL = f"sqlite:///{os.path.join(self.DATA_ROOT, 'qualivision.db')}"
            if not self.UPLOAD_DIR or self.UPLOAD_DIR == "./data/uploads":
                self.UPLOAD_DIR = os.path.join(self.DATA_ROOT, "uploads")
            if not self.HEATMAP_DIR or self.HEATMAP_DIR == "./data/heatmaps":
                self.HEATMAP_DIR = os.path.join(self.DATA_ROOT, "heatmaps")
            if not self.SAMPLES_DIR or self.SAMPLES_DIR == "./data/samples":
                self.SAMPLES_DIR = os.path.join(self.BASE_DIR, "data", "samples")

settings = Settings()

try:
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")
    if db_path:
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.HEATMAP_DIR, exist_ok=True)
    os.makedirs(settings.SAMPLES_DIR, exist_ok=True)
except Exception:
    pass

