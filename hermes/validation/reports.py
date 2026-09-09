from pydantic import BaseModel


class CheckResult(BaseModel):
    name: str
    passed: bool
    message: str | None = None
    severity: str = "error"


class ValidationReport(BaseModel):
    passed: bool = True
    checks: list[CheckResult] = []
    errors: list[str] = []
    warnings: list[str] = []

    def summary(self) -> str:
        raise NotImplementedError()

    def add_check(self, check: CheckResult) -> None:
        raise NotImplementedError()
