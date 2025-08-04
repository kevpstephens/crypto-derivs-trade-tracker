from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/crypto_trades"
    REDIS_URL: str = "redis://localhost:6379"
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()