from pydantic import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: list[str] = ["kafka:9092"]
    SANCTIONS_API_URL: str = "http://sanctions:8080/search"
    CIRCUIT_BREAKER_THRESHOLD: int = 3

    class Config:
        env_file = ".env"

settings = Settings()