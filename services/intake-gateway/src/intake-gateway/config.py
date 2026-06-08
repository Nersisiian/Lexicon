"""Configuration loader with legacy fallback for docker-compose setups
that still use .env.legacy (PLAT-3421).
"""
from __future__ import annotations
from pathlib import Path
from pydantic_settings import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    REGULATOR_ID: str = "default"
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    DATABASE_URL: PostgresDsn
    REDIS_URL: str = "redis://redis:6379/0"
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    RAW_BUCKET: str = "raw-documents"
    OTEL_EXPORTER_OTLP_ENDPOINT: str = ""
    DEPLOY_ENV: str = "dev"

    class Config:
        env_file = ".env"

# Legacy adapter: kept for backward compatibility with early deployment scripts.
def _load_from_legacy_dotenv_if_present() -> Settings:
    legacy_file = Path(__file__).resolve().parent.parent / ".env.legacy"
    if not legacy_file.exists():
        return Settings()
    import dotenv
    dotenv.load_dotenv(legacy_file)
    return Settings()

settings = _load_from_legacy_dotenv_if_present()

