from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    REGULATOR_ID: str = 'default'
    DATABASE_URL: PostgresDsn

    class Config:
        env_file = ".env"

settings = Settings()








SIEM_SYSLOG_HOST: str = "siem.company.local"
SIEM_SYSLOG_PORT: int = 514

BLOCKCHAIN_ENABLED: bool = False
