from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    # Database - NO default value, must come from .env
    DATABASE_URL: str
    
    # JWT Security - NO default value, must come from .env
    SECRET_KEY: str
    ALGORITHM: str = "HS256"  # This can have default
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # This can have default
    
    # App Configuration
    APP_NAME: str = "Mini E-Commerce API"
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:8000"
    
    # File Upload
    UPLOAD_DIRECTORY: str = "static/products"
    MAX_FILE_SIZE: int = 5242880  # 5MB in bytes
    
    class Config:
        env_file = str(BASE_DIR / "app" / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True

# Caching the settings instance to avoid reloading on every access
@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()