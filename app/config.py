from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # --- App ---
    app_name: str = "clicuster"
    app_env: Literal["development", "staging", "production"] = Field(
        default="development",
        validation_alias=AliasChoices("app_env", "ENVIRONMENT"),
    )
    debug: bool = True

    # --- API ---
    api_v1_prefix: str = "/api/v1"

    # --- CORS ---
    cors_origins: str = "http://localhost:3000,http://localhost:8000"

    # --- PostgreSQL ---
    # Прямой URL имеет приоритет. Если пуст — соберём из частей ниже.
    database_url: Optional[str] = None

    postgres_user: str = "clicuster"
    postgres_password: str = "clicuster"
    postgres_db: str = "clicuster"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    # --- Redis ---
    redis_url: Optional[str] = None
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    # --- JWT ---
    jwt_secret_key: str = Field(
        default="change-me-in-production",
        validation_alias=AliasChoices("jwt_secret_key", "SECRET_KEY"),
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("jwt_algorithm", "ALGORITHM"),
    )
    jwt_access_token_expire_minutes: int = Field(
        default=30,
        validation_alias=AliasChoices(
            "jwt_access_token_expire_minutes", "ACCESS_TOKEN_EXPIRE_MINUTES"
        ),
    )
    jwt_refresh_token_expire_days: int = Field(
        default=7,
        validation_alias=AliasChoices(
            "jwt_refresh_token_expire_days", "REFRESH_TOKEN_EXPIRE_DAYS"
        ),
    )

    @model_validator(mode="after")
    def _fill_urls(self) -> "Settings":
        if not self.database_url:
            self.database_url = (
                f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
                f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
            )
        if not self.redis_url:
            self.redis_url = f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return self

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
