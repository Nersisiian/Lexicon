from pydantic import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: list[str] = ["kafka:9092"]
    MODEL_NAME: str = "finreg-bert-classifier"
    DEVICE: str = "cpu"  # "cuda" if available in production

    class Config:
        env_file = ".env"

settings = Settings()