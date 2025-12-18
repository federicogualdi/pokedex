"""Custom exception definitions for the project."""


class BaseError(Exception):
    """Base class for all custom exceptions."""


class NotFoundError(BaseError):
    """Raised when database object does not exist."""


class InvalidArgumentError(BaseError):
    """Raised when an invalid argument is passed to a function."""


class ExecutionError(BaseError):
    """Raised when an unexpected behavior happens."""
