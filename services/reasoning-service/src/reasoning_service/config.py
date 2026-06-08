from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: list[str] = ["kafka:9092"]
    LLM_ENDPOINT: str = "http://llm:8080/v1/completions"

    class Config:
        env_file = ".env"

settings = Settings()
