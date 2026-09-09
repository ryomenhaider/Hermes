from pydantic import BaseModel


class RetryPolicy(BaseModel):
    max_retries: int = 3
    backoff_factor: float = 1.0
    retry_on: list[str] = []

    def should_retry(self, attempt: int, error: Exception) -> bool:
        raise NotImplementedError()

    def delay(self, attempt: int) -> float:
        raise NotImplementedError()
