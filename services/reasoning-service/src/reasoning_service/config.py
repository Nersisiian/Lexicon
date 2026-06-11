from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REGULATOR_ID: str = 'default'
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    LLM_ENDPOINT: str = "http://llm:8080/v1/completions"

    class Config:
        env_file = ".env"

settings = Settings()





