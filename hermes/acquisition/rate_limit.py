import asyncio


class RateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: float = 60.0) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._semaphore = asyncio.Semaphore(max_requests)

    async def acquire(self) -> None:
        raise NotImplementedError()

    async def __aenter__(self) -> "RateLimiter":
        raise NotImplementedError()

    async def __aexit__(self, *args: object) -> None:
        raise NotImplementedError()
