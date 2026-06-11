from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    SLACK_WEBHOOK_URL: str = ""
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = "noreply@regulator.internal"
    SMTP_TO: str = "compliance-team@regulator.internal"
    SMTP_TLS: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
