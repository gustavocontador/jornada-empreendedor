"""
Configuração central da aplicação usando Pydantic Settings.
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Settings da aplicação."""

    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Application
    PROJECT_NAME: str = "Jornada do Empreendedor de Sucesso"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    REPORTS_DIR: str = "./reports"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB

    # Admin
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


# Singleton instance
settings = Settings()
