class MetadataRegistry:
    def __init__(self) -> None:
        self._extractors: dict[str, object] = {}

    def register(self, name: str, extractor: object) -> None:
        raise NotImplementedError()

    def get(self, name: str) -> object | None:
        raise NotImplementedError()

    def list(self) -> list[str]:
        raise NotImplementedError()
