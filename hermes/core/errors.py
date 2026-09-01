class HermesError(Exception):
    """Base exception for all Hermes errors."""


class AcquisitionError(HermesError):
    """Failed to acquire data from source."""


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
    
class FetchingError(HermesError):
    ""


