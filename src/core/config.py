import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


def _env_file() -> str:
    """Pick env file based on APP_ENV. Defaults to .env (local dev)."""
    env = os.getenv("APP_ENV", "dev").lower()
    mapping = {
        "dev": "configs/.env",
        "sandbox": "configs/.env.sandbox",
        "production": "configs/.env.production",
    }
    return mapping.get(env, "configs/.env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_env_file(),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Ecommerce Platform"
    app_env: str = "dev"
    debug: bool = True

    database_url: str
    database_replica_url: str | None = None
    redis_url: str = "redis://localhost:6389/0"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Security flags
    show_error_details: bool = False  # controls tracebacks in 500 responses
    allowed_hosts: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()