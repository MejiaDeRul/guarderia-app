# app/config.py
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    APP_NAME: str = "Guarderia API"

    # --- CORS ---
    CORS_ORIGINS: list[str] = []
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_cors(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if v.startswith("["):
                return v
            return [x.strip() for x in v.split(",") if x.strip()]
        return v

    # --- DB (como lo dejamos antes) ---
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "guarderia"
    DATABASE_URL: Optional[str] = None
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # --- AUTH / JWT ---
    JWT_SECRET_KEY: str = "change-this-in-prod"     # ⚠️ cámbialo en .env
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60           # <- EL QUE FALTABA

settings = Settings()
