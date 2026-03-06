from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", extra="ignore")

    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    user: str = Field(default="postgres")
    password: str = Field(default="postgres")
    name: str = Field(default="landing_saas")
    echo: bool = Field(default=False)

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


settings = DatabaseSettings()
