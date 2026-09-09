from typing import Any, Literal

from pydantic import BaseModel, Field


class ResultError(BaseModel):
    """Serializable error record attached to a ``Result``."""

    code: str
    message: str
    details: dict[str, Any] | None = None


class Result(BaseModel):
    status: Literal["success", "warning", "partial", "failure"]
    data: Any = None
    errors: list[ResultError] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    def add_error(self, error: BaseException, **details: Any) -> None:
        """Record an exception as a serializable :class:`ResultError`."""
        code = type(error).__name__
        message = str(error) or code
        self.errors.append(ResultError(code=code, message=message, details=details or None))

    def is_success(self) -> bool:
        return self.status == "success" and not self.errors

    def is_failure(self) -> bool:
        return self.status == "failure" or bool(self.errors)

    def raise_if_failure(self) -> None:
        if self.errors:
            raise RuntimeError(self.errors[0].message)