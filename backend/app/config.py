
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "NMLS Radar"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nmls_radar.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_SECURITY_MD5_KEY_CHANGE_IN_PROD")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
