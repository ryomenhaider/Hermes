from hermes.core.result import Result


def fetch(source: str, **kwargs: object) -> Result:
    raise NotImplementedError()


def ingest(source: str, **kwargs: object) -> Result:
    raise NotImplementedError()


def read(path: str, **kwargs: object) -> Result:
    raise NotImplementedError()


def sync(source: str, **kwargs: object) -> Result:
    raise NotImplementedError()
