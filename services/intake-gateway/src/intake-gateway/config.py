from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

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

settings = Settings()


