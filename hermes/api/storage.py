from hermes.core.result import Result


def save(data: object, path: str, format: str = "parquet") -> Result:
    raise NotImplementedError()


def load(path: str) -> Result:
    raise NotImplementedError()


def query(data: object, **kwargs: object) -> Result:
    raise NotImplementedError()


def materialize(data: object, target: str) -> Result:
    raise NotImplementedError()
