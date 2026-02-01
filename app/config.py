"""
Application Configuration
Centralized settings management using Pydantic.
"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "GlobalTrustHub"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/globaltrusthub"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS - Allow all localhost origins for development
    CORS_ORIGINS: List[str] = [
        "http://localhost:*",
        "http://127.0.0.1:*",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5000",
        "http://localhost:53000",
        "http://localhost:55115",
        "http://localhost:56108",
        "http://localhost:58907",
        "http://localhost:60158",
        "http://localhost:62937",
        "http://127.0.0.1:8080",
        "https://globaltrusthub.com",
        "https://forexcompanion-e5a28.web.app",
    ]
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: List[str] = ["image/jpeg", "image/png", "application/pdf"]
    UPLOAD_DIR: str = "uploads"
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@globaltrusthub.com"
    
    # Firebase (for push notifications)
    FIREBASE_CREDENTIALS_PATH: str = ""
    
    # AI/ML Services
    AI_SERVICE_URL: str = "http://localhost:8001"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # seconds
    
    # Admin Configuration
    ADMIN_EMAILS: List[str] = ["sohaibdanialahmed@gmail.com"]
    
    # User Types
    USER_TYPES: List[str] = ["student", "job_seeker", "service_provider"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
