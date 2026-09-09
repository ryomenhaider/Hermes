from pydantic import BaseModel


class Filter(BaseModel):
    field: str
    operator: str
    value: object


def eq(field: str, value: object) -> Filter:
    raise NotImplementedError()


def gt(field: str, value: object) -> Filter:
    raise NotImplementedError()


def lt(field: str, value: object) -> Filter:
    raise NotImplementedError()


def gte(field: str, value: object) -> Filter:
    raise NotImplementedError()


def lte(field: str, value: object) -> Filter:
    raise NotImplementedError()


def in_list(field: str, values: list[object]) -> Filter:
    raise NotImplementedError()


def between(field: str, low: object, high: object) -> Filter:
    raise NotImplementedError()
