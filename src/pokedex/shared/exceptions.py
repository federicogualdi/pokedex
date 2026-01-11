"""Custom exception definitions for the project."""

from dataclasses import dataclass


class BaseError(Exception):
    """Base class for all custom exceptions."""


class NotFoundError(BaseError):
    """Raised when database object does not exist."""


class InvalidArgumentError(BaseError):
    """Raised when an invalid argument is passed to a function."""


class ExecutionError(BaseError):
    """Raised when an unexpected behavior happens."""


@dataclass(frozen=True)
class UpstreamError(ExecutionError):
    """Base class for upstream exceptions."""

    service: str
    method: str
    path: str
    status_code: int | None = None
    detail: str | None = None


class UpstreamServerError(UpstreamError):
    """5xx from upstream (retriable)."""


class UpstreamClientError(UpstreamError):
    """4xx from upstream (usually not retriable)."""


class UpstreamTimeoutError(UpstreamError):
    """Timeout talking to upstream (retriable)."""


class UpstreamRequestError(UpstreamError):
    """Network/DNS/connection error (retriable)."""
