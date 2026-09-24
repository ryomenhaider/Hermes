class HermesError(Exception):
    """Base exception for all Hermes errors."""


class AcquisitionError(HermesError):
    """Failed to acquire data from source."""

    def __init__(self, message: str = "", status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class ServerError(AcquisitionError):
    """The remote server returned a 5xx error (retryable)."""


class RateLimitError(AcquisitionError):
    """Rate limit exceeded; retry after delay."""

    def __init__(self, message: str = "", retry_after: float | None = None) -> None:
        super().__init__(message)
        self.retry_after = retry_after


class TimeoutError(AcquisitionError):
    """Request timed out."""


class ParseError(HermesError):
    """Failed to parse source data."""


class SchemaError(HermesError):
    """Schema-related error."""


class NormalizationError(HermesError):
    """Failed to normalize data."""


class ValidationError(HermesError):
    """Data failed validation checks."""


class StorageError(HermesError):
    """Storage operation failed."""


class QueryError(HermesError):
    """Query execution failed."""


class ConfigError(HermesError):
    """Configuration error."""


class ConnectorNotFoundError(HermesError):
    """Requested connector is not installed."""


class AuthenticationError(HermesError):
    """Missing or invalid credentials."""

    def __init__(self, message: str = "", status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class UnknownEntityTypeError(HermesError):
    """No resolver is registered for the requested entity type."""
