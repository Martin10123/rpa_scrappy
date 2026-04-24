"""
AutoFlow AI - Backend Configuration
Configuración centralizada para variables de entorno y settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # ============================================
    # Database
    # ============================================
    DATABASE_URL: str = "postgresql+asyncpg://autoflow_user:autoflow_password_dev@localhost:5432/autoflow_db"
    
    # ============================================
    # FastAPI
    # ============================================
    APP_NAME: str = "AutoFlow AI"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # ============================================
    # Claude API
    # ============================================
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # ============================================
    # Logging
    # ============================================
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instancia global de settings
settings = Settings()
