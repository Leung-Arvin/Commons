from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "OpenSpaces"
    debug: bool = False
    database_url: str = "postgresql+asyncpg://user:pass@localhost:5432/openspaces"
    test_database_url: str = "sqlite+aiosqlite:///./test.db"
    redis_url: str = "redis://localhost:6379"
    kafka_broker: str = "localhost:9092"

    model_config = {"env_prefix": "OPENSACES_", "env_file": ".env"}

settings = Settings()