from hermes.core.result import Result


def parse(data: object, **kwargs: object) -> Result:
    raise NotImplementedError()


def normalize(data: object, **kwargs: object) -> Result:
    raise NotImplementedError()


def validate(data: object, contract: object | None = None) -> Result:
    raise NotImplementedError()


def transform(data: object, fn: object | None = None, **kwargs: object) -> Result:
    raise NotImplementedError()


def profile(data: object) -> Result:
    raise NotImplementedError()


def inspect(data: object) -> Result:
    raise NotImplementedError()
