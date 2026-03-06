from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_env: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    database_url: str
    redis_url: str
    stripe_webhook_secret: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
