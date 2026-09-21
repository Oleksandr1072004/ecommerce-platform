from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="configs/.env", extra="ignore")

    app_name: str = "Ecommerce Platform"
    app_env: str = "dev"
    debug: bool = True

    database_url: str = "postgresql+psycopg2://ecom:ecom@localhost:5432/ecom"
    database_replica_url: str | None = None
    redis_url: str = "redis://localhost:6379/0"


settings = Settings()