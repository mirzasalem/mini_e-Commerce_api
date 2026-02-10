from pydantic_settings import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./ecommerce.db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # App
    APP_NAME: str = "Mini E-Commerce API"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"

 # Caching the settings instance to avoid reloading on every access
@lru_cache()


def get_settings():
    return Settings()


settings = get_settings()