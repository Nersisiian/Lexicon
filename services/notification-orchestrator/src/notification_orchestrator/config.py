from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    SLACK_WEBHOOK_URL: str = ""

    class Config:
        env_file = ".env"

settings = Settings()

