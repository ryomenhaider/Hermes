import datetime
import re
from typing import Any

try:
    import polars as pl
except ImportError:
    print("This Module Need Polars and PyArrow Installed, use pip/uv install/add hermes-plt[data] ")

from hermes.validation.errors import RuleConfigurationError, RuleExecutionError
from hermes.validation.result import RuleResult, Violation
from hermes.validation.rule import ValidationRule

_DEFAULT_MAX_VIOLATIONS = 100


def _require_column(data: pl.DataFrame, field: str, rule: str) -> None:
    if field not in data.columns:
        raise RuleExecutionError(f"{rule}: column {field!r} not found")


def _sample(
    df: pl.DataFrame,
    mask: pl.Expr,
    fields: str | list[str],
    max_n: int,
    expected: Any = None,
) -> list[Violation]:
    if max_n <= 0:
        return []
    names = [fields] if isinstance(fields, str) else list(fields)
    label = names[0] if len(names) == 1 else "+".join(names)
    flagged = df.with_row_index("__hrow__").filter(mask).head(max_n)
    out: list[Violation] = []
    for row in flagged.to_dicts():
        value = row[names[0]] if len(names) == 1 else tuple(row[n] for n in names)
        out.append(
            Violation(
                field=label,
                row=row["__hrow__"],
                value=value,
                expected=expected,
                message=f"{label} violates the constraint",
            )
        )
    return out


_TYPE_ALIASES: dict[str, str] = {
    "string": "string",
    "str": "string",
    "text": "string",
    "character": "string",
    "varchar": "string",
    "integer": "integer",
    "int": "integer",
    "int64": "integer",
    "long": "integer",
    "float": "float",
    "double": "float",
    "number": "float",
    "real": "float",
    "boolean": "boolean",
    "bool": "boolean",
    "date": "date",
    "datetime": "datetime",
    "timestamp": "datetime",
    "datetime64": "datetime",
    "decimal": "decimal",
    "numeric": "numeric",
}


def _dtype_matches(dtype: Any, type_name: str) -> bool:
    family = _TYPE_ALIASES.get(type_name.lower())
    if family is None:
        raise RuleConfigurationError(f"unsupported type name {type_name!r}")
    if family == "numeric":
        return bool(dtype.is_numeric())
    if family == "string":
        return isinstance(dtype, pl.String) or str(dtype) in ("Categorical", "Enum")
    if family == "integer":
        return bool(dtype.is_integer())
    if family == "float":
        return bool(dtype.is_float()) or isinstance(dtype, pl.Decimal)
    if family == "boolean":
        return dtype == pl.Boolean
    if family == "date":
        return dtype == pl.Date
    if family == "datetime":
        return isinstance(dtype, pl.Datetime)
    if family == "decimal":
        return isinstance(dtype, pl.Decimal)
    raise RuleConfigurationError(f"unsupported type name {type_name!r}")


def _to_reference_frame(reference: Any, rule: str) -> pl.DataFrame:
    if isinstance(reference, pl.DataFrame):
        return reference
    if isinstance(reference, pl.LazyFrame):
        return reference.collect()
    try:
        import pyarrow as pa
    except ImportError:
        pa = None
    if pa is not None and isinstance(reference, pa.Table):
        return pl.DataFrame(pl.from_arrow(reference))
    if isinstance(reference, dict):
        return pl.DataFrame([reference])
    if isinstance(reference, (list, tuple)):
        return pl.from_dicts(list(reference))
    raise RuleConfigurationError(f"{rule}: unsupported reference type {type(reference).__name__}")


def _iso(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    return str(value)


def _duration(amount: str | datetime.timedelta) -> datetime.timedelta:
    if isinstance(amount, datetime.timedelta):
        return amount
    match = re.fullmatch(r"(\d+)(s|m|h|d)", str(amount).strip().lower())
    if not match:
        raise RuleConfigurationError(f"invalid duration {amount!r}; expected e.g. '30m', '24h', '7d'")
    value, unit = int(match.group(1)), match.group(2)
    factor = {"s": 1, "m": 60, "h": 3600, "d": 86400}[unit]
    return datetime.timedelta(seconds=value * factor)


def _reference_lookup(
    data: pl.DataFrame, field: str, reference: Any, reference_field: str, rule: str
) -> tuple[pl.DataFrame, int, int]:
    ref = _to_reference_frame(reference, rule)
    if reference_field not in ref.columns:
        raise RuleExecutionError(f"{rule}: reference column {reference_field!r} not found in reference dataset")

    src = data.select(pl.col(field).alias("__v")).with_row_index("__r").filter(pl.col("__v").is_not_null())
    ref_values = ref.select(pl.col(reference_field).alias("__v")).drop_nulls().unique()
    try:
        matched = src.join(ref_values, on="__v", how="inner")
    except Exception as exc:
        raise RuleExecutionError(
            f"{rule}: cannot compare column {field!r} ({src['__v'].dtype}) with "
            f"{reference_field!r} ({ref_values['__v'].dtype}): {exc}"
        ) from exc
    missing = src.join(ref_values, on="__v", how="anti")
    return missing, matched.height, missing.height


class NotNull(ValidationRule):
    def __init__(self, field: str, *, max_violations: int = _DEFAULT_MAX_VIOLATIONS) -> None:
        self.field = field
        self.max_violations = max_violations

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        total = data.height
        null_count = data[self.field].null_count()
        null_rate = null_count / total if total else 0.0
        violations = _sample(data, pl.col(self.field).is_null(), self.field, self.max_violations, expected="not null")
        return RuleResult(
            rule=self.name,
            passed=null_count == 0,
            statistics={"total_count": total, "null_count": null_count, "null_rate": null_rate},
            violations=violations,
            message=f"Column '{self.field}' has {null_count} null value(s)",
        )


class Unique(ValidationRule):
    def __init__(self, field: str, *, max_violations: int = _DEFAULT_MAX_VIOLATIONS) -> None:
        self.field = field
        self.max_violations = max_violations

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        duplicate_count = int(data[self.field].is_duplicated().sum())
        violations = _sample(
            data, pl.col(self.field).is_duplicated(), self.field, self.max_violations, expected="unique"
        )
        return RuleResult(
            rule=self.name,
            passed=duplicate_count == 0,
            statistics={
                "total_count": data.height,
                "unique_count": data[self.field].drop_nulls().n_unique(),
                "duplicate_count": duplicate_count,
            },
            violations=violations,
            message=f"Column '{self.field}' has {duplicate_count} duplicate value(s)",
        )


class UniqueCombination(ValidationRule):
    def __init__(self, fields: list[str], *, max_violations: int = _DEFAULT_MAX_VIOLATIONS) -> None:
        self.fields = list(fields)
        self.max_violations = max_violations

    def validate(self) -> None:
        if len(self.fields) < 2:
            raise RuleConfigurationError("UniqueCombination requires at least two columns")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        missing = set(self.fields) - set(data.columns)
        if missing:
            raise RuleExecutionError(f"UniqueCombination: column(s) not found: {sorted(missing)}")
        sub = data.select(self.fields)
        keyed = sub.select(pl.struct([pl.col(c) for c in self.fields]).alias("__k"))
        duplicate_count = int(keyed.select(pl.col("__k").is_duplicated()).to_series().sum())
        unique_count = int(keyed.select(pl.col("__k").n_unique()).item())
        key = pl.struct([pl.col(c) for c in self.fields])
        return RuleResult(
            rule=self.name,
            passed=duplicate_count == 0,
            statistics={
                "total_count": sub.height,
                "unique_count": unique_count,
                "duplicate_count": duplicate_count,
            },
            violations=_sample(sub, key.is_duplicated(), self.fields, self.max_violations, expected="unique"),
            message=f"Combination {self.fields} has {duplicate_count} duplicate row(s)",
        )


class TypeCheck(ValidationRule):
    def __init__(self, target: str | dict[str, str], type_name: str | None = None) -> None:
        if isinstance(target, str):
            if type_name is None:
                raise RuleConfigurationError("TypeCheck requires a type name when target is a column")
            self.types: dict[str, str] = {target: type_name}
        else:
            self.types = dict(target)
        if not self.types or not all(isinstance(v, str) for v in self.types.values()):
            raise RuleConfigurationError("TypeCheck requires column -> type-name mappings")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        missing = set(self.types) - set(data.columns)
        if missing:
            raise RuleExecutionError(f"TypeCheck: column(s) not found: {sorted(missing)}")
        matches = {col: _dtype_matches(data[col].dtype, name) for col, name in self.types.items()}
        passed = all(matches.values())
        valid_cells = sum(data.height for col, ok in matches.items() if ok)
        invalid_cells = sum(data.height for col, ok in matches.items() if not ok)
        return RuleResult(
            rule=self.name,
            passed=passed,
            statistics={
                "expected_type": dict(self.types),
                "actual_types": {col: str(data[col].dtype) for col in self.types},
                "valid_count": valid_cells,
                "invalid_count": invalid_cells,
            },
            message="All types match" if passed else f"Type mismatch in: {[c for c, m in matches.items() if not m]}",
        )


class RangeCheck(ValidationRule):
    def __init__(
        self,
        field: str,
        min: float | None = None,
        max: float | None = None,
        *,
        max_violations: int = _DEFAULT_MAX_VIOLATIONS,
    ) -> None:
        self.field = field
        self.min = min
        self.max = max
        self.max_violations = max_violations

    def validate(self) -> None:
        if self.min is None and self.max is None:
            raise RuleConfigurationError("RangeCheck requires at least one of min or max")
        if self.min is not None and self.max is not None and self.min > self.max:
            raise RuleConfigurationError("RangeCheck: min must be <= max")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        if not data[self.field].dtype.is_numeric():
            raise RuleExecutionError(f"RangeCheck: column {self.field!r} is not numeric")

        def out_of_range(cmp: pl.Expr) -> int:
            return int(data.filter(pl.col(self.field).is_not_null() & cmp).height)

        below = out_of_range(pl.col(self.field) < self.min) if self.min is not None else 0
        above = out_of_range(pl.col(self.field) > self.max) if self.max is not None else 0
        numeric = data[self.field].drop_nulls()
        actual_min = numeric.min() if numeric.len() else None
        actual_max = numeric.max() if numeric.len() else None
        violations: list[Violation] = []
        if self.min is not None:
            violations += _sample(
                data,
                pl.col(self.field).is_not_null() & (pl.col(self.field) < self.min),
                self.field,
                self.max_violations,
                expected=f">= {self.min}",
            )
        if self.max is not None:
            violations += _sample(
                data,
                pl.col(self.field).is_not_null() & (pl.col(self.field) > self.max),
                self.field,
                self.max_violations,
                expected=f"<= {self.max}",
            )
        return RuleResult(
            rule=self.name,
            passed=below == 0 and above == 0,
            statistics={
                "min": self.min,
                "max": self.max,
                "actual_min": actual_min,
                "actual_max": actual_max,
                "below_min": below,
                "above_max": above,
                "invalid_count": below + above,
            },
            violations=violations,
            message=f"Column '{self.field}' has {below + above} value(s) outside the allowed range",
        )


class EnumCheck(ValidationRule):
    def __init__(self, field: str, allowed: list[Any], *, max_violations: int = _DEFAULT_MAX_VIOLATIONS) -> None:
        self.field = field
        self.allowed = list(allowed)
        self.max_violations = max_violations

    def validate(self) -> None:
        if not self.allowed:
            raise RuleConfigurationError("EnumCheck: allowed must not be empty")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        invalid_mask = pl.col(self.field).is_not_null() & (~pl.col(self.field).is_in(self.allowed))
        invalid_count = int(data.filter(invalid_mask).height)
        invalid_values = data.filter(invalid_mask).select(pl.col(self.field).unique()).to_series().to_list()
        return RuleResult(
            rule=self.name,
            passed=invalid_count == 0,
            statistics={
                "allowed_values": self.allowed,
                "invalid_count": invalid_count,
                "invalid_values": invalid_values,
            },
            violations=_sample(data, invalid_mask, self.field, self.max_violations, expected=self.allowed),
            message=f"Column '{self.field}' has {invalid_count} value(s) outside the allowed set",
        )


class RegexCheck(ValidationRule):
    def __init__(self, field: str, pattern: str, *, max_violations: int = _DEFAULT_MAX_VIOLATIONS) -> None:
        self.field = field
        self.pattern = pattern
        self.max_violations = max_violations
        self._compiled = re.compile(pattern)

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        tested = pl.col(self.field).cast(pl.String)
        invalid_mask = tested.is_not_null() & (~tested.str.contains(self.pattern))
        invalid_count = int(data.filter(invalid_mask).height)
        invalid_values = data.filter(invalid_mask).select(pl.col(self.field).unique()).to_series().to_list()
        return RuleResult(
            rule=self.name,
            passed=invalid_count == 0,
            statistics={
                "pattern": self.pattern,
                "valid_count": int(data.filter(tested.is_not_null() & tested.str.contains(self.pattern)).height),
                "invalid_count": invalid_count,
                "invalid_values": invalid_values,
            },
            violations=_sample(
                data, invalid_mask, self.field, self.max_violations, expected=f"matches {self.pattern!r}"
            ),
            message=f"Column '{self.field}' has {invalid_count} value(s) not matching pattern {self.pattern!r}",
        )

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "pattern": self.pattern}


class LengthCheck(ValidationRule):
    def __init__(
        self,
        field: str,
        min: int = 1,
        max: int | None = None,
        *,
        max_violations: int = _DEFAULT_MAX_VIOLATIONS,
    ) -> None:
        self.field = field
        self.min = min
        self.max = max
        self.max_violations = max_violations

    def validate(self) -> None:
        if self.min < 0:
            raise RuleConfigurationError("LengthCheck: min must be >= 0")
        if self.max is not None and self.max < self.min:
            raise RuleConfigurationError("LengthCheck: max must be >= min")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        lens = pl.col(self.field).cast(pl.String).str.len_chars()
        invalid_mask = pl.col(self.field).is_not_null() & (lens < self.min)
        if self.max is not None:
            invalid_mask = invalid_mask | (pl.col(self.field).is_not_null() & (lens > self.max))
        invalid_count = int(data.filter(invalid_mask).height)
        lens_series = data[self.field].cast(pl.String).str.len_chars().drop_nulls()
        return RuleResult(
            rule=self.name,
            passed=invalid_count == 0,
            statistics={
                "min_length": self.min,
                "max_length": self.max,
                "actual_min": lens_series.min() if lens_series.len() else None,
                "actual_max": lens_series.max() if lens_series.len() else None,
                "invalid_count": invalid_count,
            },
            violations=_sample(
                data, invalid_mask, self.field, self.max_violations, expected=f"length in [{self.min}, {self.max}]"
            ),
            message=f"Column '{self.field}' has {invalid_count} value(s) with invalid length",
        )


def _parse_date_bound(value: Any, field: str, rule: str) -> datetime.date:
    if isinstance(value, datetime.datetime):
        return value.date()
    if isinstance(value, datetime.date):
        return value
    try:
        return datetime.date.fromisoformat(str(value))
    except ValueError as exc:
        raise RuleConfigurationError(f"{rule}: invalid date {value!r} for {field!r}") from exc


def _parse_datetime_bound(value: Any, field: str, rule: str) -> datetime.datetime:
    if isinstance(value, datetime.datetime):
        return value
    if isinstance(value, datetime.date):
        return datetime.datetime(value.year, value.month, value.day)
    try:
        return datetime.datetime.fromisoformat(str(value))
    except ValueError as exc:
        raise RuleConfigurationError(f"{rule}: invalid datetime {value!r} for {field!r}") from exc


class DateRangeCheck(ValidationRule):
    def __init__(
        self, field: str, min: Any = None, max: Any = None, *, max_violations: int = _DEFAULT_MAX_VIOLATIONS
    ) -> None:
        self.field = field
        self.min = min
        self.max = max
        self.max_violations = max_violations

    def validate(self) -> None:
        if self.min is None and self.max is None:
            raise RuleConfigurationError("DateRangeCheck requires at least one of min or max")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        dtype = data[self.field].dtype
        is_datetime = isinstance(dtype, pl.Datetime)
        if not is_datetime and dtype != pl.Date:
            raise RuleExecutionError(
                f"DateRangeCheck: column {self.field!r} must be a date/datetime column, got {dtype}"
            )

        def parse_bound(value: Any) -> Any:
            if value is None:
                return None
            parse = _parse_datetime_bound if is_datetime else _parse_date_bound
            return parse(value, self.field, self.name)

        lower = parse_bound(self.min)
        upper = parse_bound(self.max)
        col = pl.col(self.field)
        before = int(data.filter(col.is_not_null() & (col < lower)).height) if lower is not None else 0
        after = int(data.filter(col.is_not_null() & (col > upper)).height) if upper is not None else 0
        valid = data[self.field].drop_nulls()
        violations: list[Violation] = []
        if lower is not None:
            violations += _sample(
                data, col.is_not_null() & (col < lower), self.field, self.max_violations, expected=f">= {self.min}"
            )
        if upper is not None:
            violations += _sample(
                data, col.is_not_null() & (col > upper), self.field, self.max_violations, expected=f"<= {self.max}"
            )
        return RuleResult(
            rule=self.name,
            passed=before == 0 and after == 0,
            statistics={
                "min": str(self.min) if self.min is not None else None,
                "max": str(self.max) if self.max is not None else None,
                "actual_min": _iso(valid.min()),
                "actual_max": _iso(valid.max()),
                "before_min": before,
                "after_max": after,
                "invalid_count": before + after,
            },
            violations=violations,
            message=f"Column '{self.field}' has {before + after} date(s) outside the allowed range",
        )


class DateOrderCheck(ValidationRule):
    def __init__(self, first: str, second: str | None = None, *, max_violations: int = _DEFAULT_MAX_VIOLATIONS) -> None:
        self.first = first
        self.second = second
        self.max_violations = max_violations

    def _require_temporal(self, data: pl.DataFrame, field: str) -> None:
        _require_column(data, field, self.name)
        dtype = data[field].dtype
        if not isinstance(dtype, pl.Datetime) and dtype != pl.Date:
            raise RuleExecutionError(f"DateOrderCheck: column {field!r} must be a date/datetime column, got {dtype}")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        self._require_temporal(data, self.first)
        if self.second is not None:
            self._require_temporal(data, self.second)
            col_a, col_b = pl.col(self.first), pl.col(self.second)
            invalid_mask = col_a.is_not_null() & col_b.is_not_null() & (col_a > col_b)
            first_violation = _first_row(data, invalid_mask, self.first, self.second)
            out_of_order = int(data.filter(invalid_mask).height)
            mode = "pairwise"
        else:
            prev_max = pl.col(self.first).cum_max().shift(1)
            col = pl.col(self.first)
            invalid_mask = col.is_not_null() & prev_max.is_not_null() & (col < prev_max)
            first_violation = _first_row(data, invalid_mask, self.first)
            out_of_order = int(data.filter(invalid_mask).height)
            mode = "sequence"
        violation_fields = [self.first, self.second] if self.second else self.first
        return RuleResult(
            rule=self.name,
            passed=out_of_order == 0,
            statistics={
                "mode": mode,
                "invalid_count": out_of_order,
                "out_of_order_count": out_of_order,
                "first_violation": first_violation,
            },
            violations=_sample(
                data, invalid_mask, violation_fields, self.max_violations, expected="chronological order"
            ),
            message=f"Column(s) have {out_of_order} out-of-order value(s)",
        )


def _first_row(data: pl.DataFrame, mask: pl.Expr, *fields: str) -> dict[str, Any] | None:
    rows = data.with_row_index("__hrow__").filter(mask).head(1).to_dicts()
    if not rows:
        return None
    row = rows[0]
    out: dict[str, Any] = {"row": row["__hrow__"]}
    for field in fields:
        out[field] = _json_safe_value(row[field])
    return out


def _json_safe_value(value: Any) -> Any:
    if isinstance(value, (datetime.datetime, datetime.date)):
        return value.isoformat()
    return value


class SchemaCheck(ValidationRule):
    def __init__(self, expected: dict[str, str]) -> None:
        self.expected = dict(expected)
        if not self.expected:
            raise RuleConfigurationError("SchemaCheck: expected schema must not be empty")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        actual = set(data.columns)
        expected_set = set(self.expected)
        missing = sorted(expected_set - actual)
        unexpected = sorted(actual - expected_set)
        mismatches = []
        for col, type_name in self.expected.items():
            if col not in actual:
                continue
            family = _TYPE_ALIASES.get(type_name.lower())
            if family is None:
                raise RuleConfigurationError(f"SchemaCheck: unsupported type name {type_name!r}")
            if not _dtype_matches(data[col].dtype, type_name):
                mismatches.append({"column": col, "expected": type_name, "actual": str(data[col].dtype)})
        passed = not missing and not unexpected and not mismatches
        return RuleResult(
            rule=self.name,
            passed=passed,
            statistics={
                "missing_columns": missing,
                "unexpected_columns": unexpected,
                "type_mismatches": mismatches,
            },
            message=f"{len(missing)} missing, {len(unexpected)} unexpected, {len(mismatches)} type mismatch(es)",
        )


class RowCountCheck(ValidationRule):
    def __init__(self, min: int | None = None, max: int | None = None, exact: int | None = None) -> None:
        self.min = min
        self.max = max
        self.exact = exact
        self.validate()

    def validate(self) -> None:
        if self.exact is not None and (self.min is not None or self.max is not None):
            raise RuleConfigurationError("RowCountCheck: exact cannot be combined with min/max")
        if self.exact is None and self.min is None and self.max is None:
            raise RuleConfigurationError("RowCountCheck requires exact or min/max")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        count = data.height
        if self.exact is not None:
            passed = count == self.exact
        else:
            passed = (self.min is None or count >= self.min) and (self.max is None or count <= self.max)
        bounds = f"exactly {self.exact}" if self.exact is not None else f"[{self.min}, {self.max}]"
        return RuleResult(
            rule=self.name,
            passed=passed,
            statistics={
                "actual_count": count,
                "expected_min": self.min,
                "expected_max": self.max,
                "expected_exact": self.exact,
            },
            message=f"Dataset has {count} row(s), expected {bounds}",
        )


class ColumnCheck(ValidationRule):
    def __init__(self, required: list[str], *, allow_extra: bool = True) -> None:
        self.required = list(required)
        self.allow_extra = allow_extra
        if not self.required:
            raise RuleConfigurationError("ColumnCheck: required must not be empty")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        actual = set(data.columns)
        missing = sorted(set(self.required) - actual)
        unexpected = sorted(actual - set(self.required)) if not self.allow_extra else []
        passed = not missing and not unexpected
        return RuleResult(
            rule=self.name,
            passed=passed,
            statistics={"missing_columns": missing, "unexpected_columns": unexpected},
            message=f"{len(missing)} missing, {len(unexpected)} unexpected column(s)",
        )


class NullRateCheck(ValidationRule):
    def __init__(self, field: str, max_rate: float) -> None:
        self.field = field
        self.max_rate = max_rate
        self.validate()

    def validate(self) -> None:
        if not 0.0 <= self.max_rate <= 1.0:
            raise RuleConfigurationError("NullRateCheck: max_rate must be between 0 and 1")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        total = data.height
        null_count = data[self.field].null_count()
        null_rate = null_count / total if total else 0.0
        return RuleResult(
            rule=self.name,
            passed=null_rate <= self.max_rate,
            statistics={
                "total_count": total,
                "null_count": null_count,
                "null_rate": null_rate,
                "allowed_rate": self.max_rate,
            },
            message=f"Column '{self.field}' has null rate {null_rate:.3f} (allowed {self.max_rate})",
        )


class DuplicateCheck(ValidationRule):
    def __init__(self, columns: list[str] | None = None) -> None:
        self.columns = list(columns) if columns is not None else None

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        fields = self.columns or data.columns
        missing = set(fields) - set(data.columns)
        if missing:
            raise RuleExecutionError(f"DuplicateCheck: column(s) not found: {sorted(missing)}")
        sub = data.select(fields)
        keyed = sub.select(pl.struct([pl.col(c) for c in fields]).alias("__k"))
        dup_series = keyed.select(pl.col("__k").is_duplicated()).to_series()
        duplicated = keyed.filter(pl.col("__k").is_duplicated())
        duplicate_rows = int(dup_series.sum())
        return RuleResult(
            rule=self.name,
            passed=duplicate_rows == 0,
            statistics={
                "duplicate_row_count": duplicate_rows,
                "duplicate_group_count": (
                    int(duplicated.select(pl.col("__k").n_unique()).item()) if duplicated.height else 0
                ),
            },
            message=f"Dataset has {duplicate_rows} duplicate row(s) over {fields}",
        )


class FreshnessCheck(ValidationRule):
    def __init__(self, field: str, max_age: str | datetime.timedelta, now: datetime.datetime | None = None) -> None:
        self.field = field
        self.max_age = max_age
        self.allowed = _duration(max_age)
        self._now = now

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        dtype = data[self.field].dtype
        is_datetime = isinstance(dtype, pl.Datetime)
        if not is_datetime and dtype != pl.Date:
            raise RuleExecutionError(
                f"FreshnessCheck: column {self.field!r} must be a date/datetime column, got {dtype}"
            )
        time_zone = dtype.time_zone if isinstance(dtype, pl.Datetime) else None

        now: Any = self._now
        if now is None and context is not None:
            now = context.get("now")
        latest: Any = data[self.field].max()
        if latest is None:
            raise RuleExecutionError(f"FreshnessCheck: column {self.field!r} has no non-null values")

        if is_datetime:
            if now is None:
                now = datetime.datetime.now(datetime.UTC)
            if time_zone is None and now.tzinfo is not None:
                now = now.replace(tzinfo=None)
            if now.tzinfo is not None and latest.tzinfo is None and time_zone is not None:
                latest = latest.replace(tzinfo=datetime.UTC)
            age_seconds = (now - latest).total_seconds()
            age_text = f"{age_seconds / 3600:.2f}h"
        else:
            now_date = (now or datetime.datetime.now(datetime.UTC)).date()
            age_days = (now_date - latest).days
            age_seconds = age_days * 86400
            age_text = f"{age_days}d"

        return RuleResult(
            rule=self.name,
            passed=datetime.timedelta(seconds=age_seconds) <= self.allowed,
            statistics={
                "latest_value": latest.isoformat(),
                "age": age_text,
                "allowed_age": str(self.max_age),
            },
            message=f"Column '{self.field}' is {age_text} old (allowed {self.max_age})",
        )


class CompletenessCheck(ValidationRule):
    def __init__(self, required: list[str], min_rate: float = 1.0) -> None:
        self.required = list(required)
        self.min_rate = min_rate

    def validate(self) -> None:
        if not self.required:
            raise RuleConfigurationError("CompletenessCheck: required must not be empty")
        if not 0.0 <= self.min_rate <= 1.0:
            raise RuleConfigurationError("CompletenessCheck: min_rate must be between 0 and 1")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        missing = set(self.required) - set(data.columns)
        if missing:
            raise RuleExecutionError(f"CompletenessCheck: column(s) not found: {sorted(missing)}")
        total = data.height
        complete_mask = pl.all_horizontal(*[pl.col(c).is_not_null() for c in self.required])
        complete_count = int(data.filter(complete_mask).height)
        complete_rate = complete_count / total if total else 0.0
        return RuleResult(
            rule=self.name,
            passed=complete_rate >= self.min_rate,
            statistics={
                "complete_count": complete_count,
                "incomplete_count": total - complete_count,
                "completeness_rate": complete_rate,
                "required_rate": self.min_rate,
            },
            message=f"{total - complete_count} incomplete row(s) of {total}",
        )


class ReferentialCheck(ValidationRule):
    def __init__(
        self,
        field: str,
        reference: Any,
        reference_field: str,
        *,
        max_violations: int = _DEFAULT_MAX_VIOLATIONS,
    ) -> None:
        self.field = field
        self.reference = reference
        self.reference_field = reference_field
        self.max_violations = max_violations

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        missing, matched, missing_count = _reference_lookup(
            data, self.field, self.reference, self.reference_field, self.name
        )
        violations = [
            Violation(
                field=self.field,
                row=row["__r"],
                value=row["__v"],
                expected="present in reference",
                message=f"{self.field} has no match in {self.reference_field}",
            )
            for row in missing.head(self.max_violations).to_dicts()
        ]
        return RuleResult(
            rule=self.name,
            passed=missing_count == 0,
            statistics={
                "missing_reference_count": missing_count,
                "matched_count": matched,
                "missing_references": missing.head(self.max_violations).select("__v").to_series().to_list(),
            },
            violations=violations,
            message=f"{missing_count} value(s) have no match in the reference",
        )


class ForeignKeyCheck(ValidationRule):
    def __init__(
        self,
        column: str,
        reference: Any,
        reference_column: str,
        *,
        max_violations: int = _DEFAULT_MAX_VIOLATIONS,
    ) -> None:
        self.column = column
        self.reference = reference
        self.reference_column = reference_column
        self.max_violations = max_violations

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.column, self.name)
        missing, matched, missing_count = _reference_lookup(
            data, self.column, self.reference, self.reference_column, self.name
        )
        violations = [
            Violation(
                field=self.column,
                row=row["__r"],
                value=row["__v"],
                expected="present in reference",
                message=f"{self.column} has no match in {self.reference_column}",
            )
            for row in missing.head(self.max_violations).to_dicts()
        ]
        return RuleResult(
            rule=self.name,
            passed=missing_count == 0,
            statistics={
                "invalid_count": missing_count,
                "matched_count": matched,
                "missing_keys": missing.head(self.max_violations).select("__v").to_series().to_list(),
            },
            violations=violations,
            message=f"{missing_count} value(s) have no matching foreign key",
        )


_PATTERNS: dict[str, str] = {
    "LEI": r"^[A-Z0-9]{18}[0-9]{2}$",
    "ISIN": r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$",
    "CUSIP": r"^[A-Z0-9]{8}[0-9]$",
    "SEDOL": r"^[A-Z0-9]{6}[0-9]$",
    "CIK": r"^\d{1,10}$",
    "ticker": r"^[A-Z]{1,5}$",
    "email": r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    "URL": r"^https?://[^\s]+$",
}


def register_pattern(name: str, regex: str) -> None:

    re.compile(regex)
    _PATTERNS[name] = regex


class PatternCheck(ValidationRule):
    def __init__(self, field: str, pattern: str, *, max_violations: int = _DEFAULT_MAX_VIOLATIONS) -> None:
        self.field = field
        self.pattern_name = pattern
        self.pattern = _pattern_regex(pattern)
        self.max_violations = max_violations

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        tested = pl.col(self.field).cast(pl.String)
        invalid_mask = tested.is_not_null() & (~tested.str.contains(self.pattern))
        invalid_count = int(data.filter(invalid_mask).height)
        invalid_values = data.filter(invalid_mask).select(pl.col(self.field).unique()).to_series().to_list()
        return RuleResult(
            rule=self.name,
            passed=invalid_count == 0,
            statistics={
                "pattern": self.pattern_name,
                "valid_count": int(data.filter(tested.is_not_null() & tested.str.contains(self.pattern)).height),
                "invalid_count": invalid_count,
                "invalid_values": invalid_values,
            },
            violations=_sample(
                data, invalid_mask, self.field, self.max_violations, expected=f"matches {self.pattern_name!r}"
            ),
            message=f"Column '{self.field}' has {invalid_count} value(s) not matching pattern {self.pattern_name!r}",
        )

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "pattern": self.pattern_name}


def _pattern_regex(name: str) -> str:
    if name in _PATTERNS:
        return _PATTERNS[name]
    try:
        re.compile(name)
        return name
    except re.error as exc:
        raise RuleConfigurationError(f"PatternCheck: unknown pattern {name!r} or invalid regex: {exc}") from exc


class ConstantCheck(ValidationRule):
    def __init__(self, field: str, expected: Any = None) -> None:
        self.field = field
        self.expected = expected

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        unique_count = data[self.field].drop_nulls().n_unique()
        values = data[self.field].drop_nulls().unique().to_list()
        value = values[0] if len(values) == 1 else None
        passed = unique_count <= 1
        if passed and self.expected is not None:
            passed = value == self.expected
        return RuleResult(
            rule=self.name,
            passed=passed,
            statistics={"unique_count": unique_count, "value": value},
            message=f"Column '{self.field}' has {unique_count} unique value(s)",
        )


class CardinalityCheck(ValidationRule):
    def __init__(
        self, field: str, min: int = 1, max: int | None = None, *, max_violations: int = _DEFAULT_MAX_VIOLATIONS
    ) -> None:
        self.field = field
        self.min = min
        self.max = max
        self.max_violations = max_violations

    def validate(self) -> None:
        if self.min < 0:
            raise RuleConfigurationError("CardinalityCheck: min must be >= 0")
        if self.max is not None and self.max < self.min:
            raise RuleConfigurationError("CardinalityCheck: max must be >= min")

    def check(self, data: pl.DataFrame, context: Any = None) -> RuleResult:
        _require_column(data, self.field, self.name)
        unique_count = data[self.field].drop_nulls().n_unique()
        passed = unique_count >= self.min and (self.max is None or unique_count <= self.max)
        return RuleResult(
            rule=self.name,
            passed=passed,
            statistics={
                "unique_count": unique_count,
                "expected_min": self.min,
                "expected_max": self.max,
            },
            message=f"Column '{self.field}' has {unique_count} unique value(s)",
        )


__all__ = [
    "NotNull",
    "Unique",
    "UniqueCombination",
    "TypeCheck",
    "RangeCheck",
    "EnumCheck",
    "RegexCheck",
    "LengthCheck",
    "DateRangeCheck",
    "DateOrderCheck",
    "SchemaCheck",
    "RowCountCheck",
    "ColumnCheck",
    "NullRateCheck",
    "DuplicateCheck",
    "FreshnessCheck",
    "CompletenessCheck",
    "ReferentialCheck",
    "ForeignKeyCheck",
    "PatternCheck",
    "ConstantCheck",
    "CardinalityCheck",
    "register_pattern",
]
