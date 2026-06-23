from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://floorsense:floorsense@localhost:5433/floorsense"
    keycloak_url: str = "http://localhost:8080"
    keycloak_realm: str = "floorsense"
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    class Config:
        env_prefix = "MAP_"

settings = Settings()