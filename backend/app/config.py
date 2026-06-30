from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Commons"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5433/commons"
    test_database_url: str = "sqlite+aiosqlite:///./test.db"
    redis_url: str = "redis://localhost:6379"
    kafka_broker: str = "localhost:9092"

    model_config = {"env_prefix": "COMMONS_", "env_file": ".env"}

settings = Settings()