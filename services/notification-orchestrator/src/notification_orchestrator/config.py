from pydantic import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: list[str] = ["kafka:9092"]
    SLACK_WEBHOOK_URL: str = ""

    class Config:
        env_file = ".env"

settings = Settings()