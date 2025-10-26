import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
load_dotenv()
class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("POSTGRES_URL")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        case_sensitive = True

settings = Settings()
