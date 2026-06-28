import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://test:test@postgres:5432/test")
