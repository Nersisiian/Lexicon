from pydantic import BaseSettings, PostgresDsn

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = ".env"

settings = Settings()