from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    KAFKA_BOOTSTRAP_SERVERS: list[str] = ["kafka:9092"]

    class Config:
        env_file = ".env"

settings = Settings()