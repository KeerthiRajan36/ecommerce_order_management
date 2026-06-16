from pydantic_settings import BaseSettings
from typing import Optional, List


class Settings(BaseSettings):
    # Database - SQLite
    DATABASE_URL: str = "sqlite:///./ecommerce.db"
    
    # JWT
    SECRET_KEY: str = "ECOMM_KEY"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@ecommerce.com"
    
    # Application
    APP_NAME: str = "E-Commerce API"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    ALLOWED_ORIGINS:str = "http://localhost:3000,http://localhost:8000"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


settings = Settings()