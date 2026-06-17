from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REGULATOR_ID: str = 'default'
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    MODEL_PATH: str = "models/fraud_ensemble.pkl"
    # A/B testing
    AB_ENABLE_MODEL_B: bool = False
    AB_TRAFFIC_SPLIT: float = 0.1

    class Config:
        env_file = ".env"

settings = Settings()