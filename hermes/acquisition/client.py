from typing import Any


class Client:
    def __init__(
        self,
        timeout: float = 30.0,
        retries: int = 3,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.timeout = timeout
        self.retries = retries
        self.headers = headers or {}

    async def get(self, url: str, **kwargs: Any) -> dict:
        raise NotImplementedError()

    async def post(self, url: str, **kwargs: Any) -> dict:
        raise NotImplementedError()

    async def close(self) -> None:
        raise NotImplementedError()
