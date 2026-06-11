from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    MODEL_PATH: str = "models/fraud_ensemble.pkl"

    class Config:
        env_file = ".env"

settings = Settings()



