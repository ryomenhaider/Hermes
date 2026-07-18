from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Callable

from sqlalchemy import ClauseElement, Column, Table, and_, not_, or_
from sqlalchemy import types as sa_types


class UnknownColumnError(KeyError):
    pass


class UnsupportedOperatorError(ValueError):
    pass


class TypeCoercionError(TypeError):
    pass


OPERATOR_MAP: dict[str, Callable[[Column, Any], ClauseElement]] = {}


def register_operator(name: str, fn: Callable[[Column, Any], ClauseElement]) -> None:
    OPERATOR_MAP[name] = fn


register_operator("eq", lambda col, v: col == v)
register_operator("neq", lambda col, v: col != v)
register_operator("gt", lambda col, v: col > v)
register_operator("gte", lambda col, v: col >= v)
register_operator("lt", lambda col, v: col < v)
register_operator("lte", lambda col, v: col <= v)
register_operator("in", lambda col, v: col.in_(v))
register_operator("not_in", lambda col, v: col.notin_(v))
register_operator("like", lambda col, v: col.like(v))
register_operator("ilike", lambda col, v: col.ilike(v))
register_operator("is", lambda col, v: col.is_(v))
register_operator("is_not", lambda col, v: col.isnot(v))


TYPE_COERCERS: dict[type, Callable[[Any], Any]] = {
    sa_types.Integer: int,
    sa_types.SmallInteger: int,
    sa_types.BigInteger: int,
    sa_types.Numeric: Decimal,
    sa_types.Float: float,
    sa_types.REAL: float,
    sa_types.Double: float,
    sa_types.String: str,
    sa_types.Text: str,
    sa_types.Unicode: str,
    sa_types.Boolean: lambda v: v if isinstance(v, bool) else v.lower() in ("true", "1", "yes"),
    sa_types.Date: lambda v: v if isinstance(v, date) else date.fromisoformat(v),
    sa_types.DateTime: lambda v: v if isinstance(v, datetime) else datetime.fromisoformat(v),
    sa_types.TIMESTAMP: lambda v: v if isinstance(v, datetime) else datetime.fromisoformat(v),
}


class FilterBuilder:
    def __init__(self, strict: bool = False):
        self._operators: dict[str, Callable[[Column, Any], ClauseElement]] = dict(OPERATOR_MAP)
        self.strict = strict

    def build(self, table: Table, filters: dict | None) -> ClauseElement | None:
        if not filters:
            return None
        return self._build_node(filters, table)

    def _build_node(self, node: Any, table: Table) -> ClauseElement | None:
        if not isinstance(node, dict):
            return None

        clauses: list[ClauseElement] = []
        for key, value in node.items():
            if key == "or":
                sub = [self._build_node(item, table) for item in value]
                sub = [s for s in sub if s is not None]
                if sub:
                    clauses.append(or_(*sub))
            elif key == "and":
                sub = [self._build_node(item, table) for item in value]
                sub = [s for s in sub if s is not None]
                if sub:
                    clauses.append(and_(*sub))
            elif key == "not":
                sub = self._build_node(value, table)
                if sub is not None:
                    clauses.append(not_(sub))
            else:
                clause = self._build_leaf(key, value, table)
                if clause is not None:
                    clauses.append(clause)

        if not clauses:
            return None
        return and_(*clauses) if len(clauses) > 1 else clauses[0]

    def _build_leaf(self, column_name: str, value: Any, table: Table) -> ClauseElement | None:
        if column_name not in table.columns:
            if self.strict:
                raise UnknownColumnError(f"Unknown column: {column_name!r}")
            return None

        col = table.columns[column_name]
        col_type = type(col.type)

        if isinstance(value, dict):
            sub_clauses: list[ClauseElement] = []
            for op, operand in value.items():
                fn = self._operators.get(op)
                if fn is None:
                    raise UnsupportedOperatorError(
                        f"Unsupported operator {op!r} for column {column_name!r}. "
                        f"Use register_operator() to add custom operators."
                    )
                coerced = self._coerce(col_type, column_name, operand)
                sub_clauses.append(fn(col, coerced))
            return and_(*sub_clauses) if sub_clauses else None

        return col == self._coerce(col_type, column_name, value)

    def _coerce(self, col_type: type, column_name: str, value: Any) -> Any:
        coercer = TYPE_COERCERS.get(col_type)
        if coercer is None:
            return value
        try:
            return coercer(value)
        except (ValueError, TypeError) as exc:
            raise TypeCoercionError(
                f"Cannot coerce value {value!r} to type {col_type.__name__} "
                f"for column {column_name!r}"
            ) from exc
