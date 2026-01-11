"""Application settings module."""

import sys

from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class CommonSettings(BaseSettings):
    """Common settings for the application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=True,
    )


class CacheSettings(CommonSettings):
    """Cache settings."""

    enabled: bool = Field(default=True, validation_alias="CACHE_ENABLED")
    ttl_seconds: int = Field(default=86400, validation_alias="CACHE_TTL_SECONDS")
    maxsize: int = Field(default=2048, validation_alias="CACHE_MAXSIZE")


class SentrySettings(CommonSettings):
    """Sentry settings."""

    enabled: bool = Field(default=False, validation_alias="SENTRY_ENABLED")
    dsn: str | None = Field(default=None, validation_alias="SENTRY_DSN")
    environment: str = Field(default="local", validation_alias="SENTRY_ENVIRONMENT")
    release: str | None = Field(default=None, validation_alias="SENTRY_RELEASE")
    traces_sample_rate: float = Field(default=0.0, validation_alias="SENTRY_TRACES_SAMPLE_RATE")  # performance
    profiles_sample_rate: float = Field(default=0.0, validation_alias="SENTRY_PROFILES_SAMPLE_RATE")  # profiling
    send_default_pii: bool = Field(default=False, validation_alias="SENTRY_SEND_DEFAULT_PII")


class RetrySettings(CommonSettings):
    """Retry settings."""

    enabled: bool = Field(default=True, validation_alias="RETRY_ENABLED")
    attempts: int = Field(default=3, validation_alias="RETRY_ATTEMPTS")


class Settings(CommonSettings):
    """Application settings.

    Args:
        BaseSettings (BaseSettings): pydantic BaseSettings class
    """

    debug: bool = Field(False, validation_alias="DEBUG")
    wait_for_debugger_connected: bool = Field(False, validation_alias="WAIT_FOR_DEBUGGER")
    log_level: str = Field("INFO", validation_alias="LOG_LEVEL")

    preferred_language: str = Field(
        "en",
        description="language name for pokemon description",
        validation_alias="PREFERRED_LANGUAGE",
    )

    # External services
    pokeapi_base_url: str = Field(default="https://pokeapi.co/api/v2", validation_alias="POKEAPI_BASE_URL")
    funtranslations_base_url: str = Field(
        default="https://api.funtranslations.com/translate",
        validation_alias="FUNTRANSLATIONS_BASE_URL",
    )
    funtranslations_shakespeare_path: str = Field(
        default="shakespeare",
        validation_alias="FUNTRANSLATIONS_SHAKESPEARE_PATH",
    )
    funtranslations_yoda_path: str = Field(default="yoda", validation_alias="FUNTRANSLATIONS_YODA_PATH")

    # HTTP
    http_timeout_seconds: float = Field(default=5.0, validation_alias="HTTP_TIMEOUT_SECONDS")

    # Cache
    cache: CacheSettings = Field(default_factory=CacheSettings)

    # Sentry
    sentry: SentrySettings = Field(default_factory=SentrySettings)

    # Retry
    retry: RetrySettings = Field(default_factory=RetrySettings)

    def __init__(self, *args, **kwargs) -> None:
        """Init settings."""
        super().__init__(*args, **kwargs)
        self._set_log_level()

    def _set_log_level(self):
        try:
            logger.remove(0)
        except ValueError:
            logger.debug("No default logger found, already removed")
        try:
            # create only one logger sink, if not already created
            if not logger._core.handlers:  # noqa: SLF001
                logger.add(sys.stderr, level=self.log_level)
                logger.debug(f"Logger initialized in this component with log level: {self.log_level}")
            else:
                logger.debug("Logger already initialized in another component, use that one")
        except ValueError:
            logger.exception("Error setting log level")


def get_logger():  # noqa: ANN201
    """Get logger."""
    return logger


settings = Settings()
