from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

