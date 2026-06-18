from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REGULATOR_ID: str = 'default'
    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    MODEL_NAME: str = "finreg-bert-classifier"
    DEVICE: str = "cpu"  # "cuda" if available in production

    class Config:
        env_file = ".env"

settings = Settings()






MODEL_PATH: str = '/models/classifier_model.pkl'
