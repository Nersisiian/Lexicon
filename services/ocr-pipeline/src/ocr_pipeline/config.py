from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: list[str] = ["kafka:9092"]
    OCR_BACKEND: str = "paddle"  # 'paddle' or 'legacy_tesseract'
    MAX_PAGES_PER_DOC: int = 20
    PROCESSING_TIMEOUT: int = 30  # seconds per document

    class Config:
        env_file = ".env"

settings = Settings()
