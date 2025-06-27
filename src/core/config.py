from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logging import LogLevel


class AppSettings(BaseSettings):
    DEBUG: bool = False
    LOG_LEVEL: str = LogLevel.INFO
    SECRET_KEY: str = Field(..., description="Django secret key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_TTL: int = 15 * 60  # second (15 mins)
    REFRESH_TOKEN_TTL: int = 60 * 60 * 24  # second (1 day)

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


settings = AppSettings()
