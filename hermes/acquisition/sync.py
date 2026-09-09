from datetime import datetime


class SyncState:
    def __init__(self) -> None:
        self.last_sync: datetime | None = None
        self.cursor: object | None = None

    def update(self, cursor: object | None = None) -> None:
        raise NotImplementedError()

    def needs_sync(self, interval: str) -> bool:
        raise NotImplementedError()

    def get_cursor(self) -> object | None:
        raise NotImplementedError()
