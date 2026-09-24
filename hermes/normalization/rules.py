import math
import re
from typing import Any, Literal, cast

import polars as pl

from hermes.normalization.constants import (
    _CAST_TYPES,
    _CURRENCY_ALIASES,
    _DEFAULT_DATE_FORMATS,
    _DEFAULT_FALSE,
    _DEFAULT_NULL_VALUES,
    _DEFAULT_TRUE,
    _PERIOD_RE,
    _UNIT_FACTORS,
    _UNIT_SYMBOLS,
)
from hermes.normalization.errors import RuleConfigurationError, RuleExecutionError, TransformationError
from hermes.normalization.rule import NormalizationRule


def _string_expr(
    col: str,
    *,
    strip: bool = False,
    collapse: bool = False,
    unicode_norm: str | None = None,
    case: str | None = None,
) -> pl.Expr:

    e: pl.Expr = pl.col(col).cast(pl.String)
    if unicode_norm:
        e = e.str.normalize(cast(Literal["NFC", "NFKC", "NFD", "NFKD"], unicode_norm))
    if strip:
        e = e.str.strip_chars()
    if collapse:
        e = e.str.replace_all(r"\s+", " ")
    if case == "lower":
        e = e.str.to_lowercase()
    elif case == "upper":
        e = e.str.to_uppercase()
    elif case == "title":
        e = e.map_elements(str.title, return_dtype=pl.String)
    return e


def _map_column(
    df: pl.DataFrame,
    col: str,
    mapping: dict[Any, Any],
    *,
    case_insensitive: bool = False,
    default: Any = None,
) -> pl.DataFrame:

    if not mapping:
        return df
    src = pl.col(col).cast(pl.String) if case_insensitive else pl.col(col)
    lookup = src.str.to_lowercase() if case_insensitive else src
    table = {str(k).lower(): v for k, v in mapping.items()} if case_insensitive else dict(mapping)
    default = pl.col(col) if default is None else default
    return df.with_columns(lookup.replace_strict(table, default=default).alias(col))


class Rename(NormalizationRule):
    def __init__(self, rename: dict[str, str]) -> None:
        self.rename_map = dict(rename)
        self.validate()

    def validate(self) -> None:
        if not self.rename_map:
            raise RuleConfigurationError("Rename requires a non-empty mapping")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        missing = set(self.rename_map) - set(data.columns)
        if missing:
            raise RuleExecutionError(f"Rename: column(s) not found: {sorted(missing)}")
        return data.rename(self.rename_map)

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "rename": self.rename_map}


class Cast(NormalizationRule):
    def __init__(self, target: str | dict[str, str], type_name: str | None = None, *, strict: bool = True) -> None:
        self.strict = strict
        casts = {target: type_name} if isinstance(target, str) else dict(target)
        if not casts:
            raise RuleConfigurationError("Cast requires at least one column")
        if not all(isinstance(v, str) for v in casts.values()):
            raise RuleConfigurationError("Cast type must be given as a type name string or a polars dtype")

        self.casts: dict[str, Any] = {}
        for col, type_str in casts.items():
            dtype: Any = type_str
            if isinstance(dtype, str):
                if dtype not in _CAST_TYPES:
                    raise RuleConfigurationError(
                        f"Cast: unsupported type {type_str!r} for column {col!r}. "
                        f"Supported: {sorted(_CAST_TYPES)} or pass a polars dtype directly."
                    )
                dtype = _CAST_TYPES[dtype]
            self.casts[col] = dtype
        self.validate()

    def validate(self) -> None:
        if not self.casts:
            raise RuleConfigurationError("Cast requires at least one column")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        missing = set(self.casts) - set(data.columns)
        if missing:
            raise RuleExecutionError(f"Cast: column(s) not found: {sorted(missing)}")

        def cast_expr(col: str, dtype: Any) -> pl.Expr:
            try:
                return pl.col(col).cast(dtype, strict=self.strict)
            except Exception as exc:
                raise TransformationError(f"Cast: cannot cast column {col!r} to {dtype}: {exc}") from exc

        return data.with_columns(cast_expr(col, dtype) for col, dtype in self.casts.items())

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "casts": {k: str(v) for k, v in self.casts.items()}, "strict": self.strict}


class NormalizeString(NormalizationRule):
    def __init__(
        self,
        field: str,
        *,
        strip: bool = True,
        collapse_whitespace: bool = True,
        unicode_norm: str | None = "NFKC",
        case: Literal["lower", "upper", "title", None] = None,
    ) -> None:
        self.field = field
        self.strip = strip
        self.collapse = collapse_whitespace
        self.unicode_norm = unicode_norm
        self.case = case

    def validate(self) -> None:
        if self.case not in (None, "lower", "upper", "title"):
            raise RuleConfigurationError(f"NormalizeString: invalid case {self.case!r}")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"NormalizeString: column {self.field!r} not found")
        expr = _string_expr(
            self.field,
            strip=self.strip,
            collapse=self.collapse,
            unicode_norm=self.unicode_norm,
            case=self.case,
        )
        return data.with_columns(expr.alias(self.field))

    def describe(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "field": self.field,
            "strip": self.strip,
            "collapse_whitespace": self.collapse,
            "unicode": self.unicode_norm,
            "case": self.case,
        }


class NormalizeNull(NormalizationRule):
    def __init__(self, fields: str | list[str] | None = None, null_values: tuple[str, ...] | None = None) -> None:
        self.fields = [fields] if isinstance(fields, str) else fields
        self.null_values = tuple(null_values) if null_values is not None else _DEFAULT_NULL_VALUES

    def validate(self) -> None:
        if not self.null_values:
            raise RuleConfigurationError("NormalizeNull: null_values must not be empty")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        fields = self.fields or [c for c in data.columns if data[c].dtype == pl.String]
        missing = set(fields) - set(data.columns)
        if missing:
            raise RuleExecutionError(f"NormalizeNull: column(s) not found: {sorted(missing)}")
        nulls = list(self.null_values)
        result = data
        for col in fields:
            if result[col].dtype != pl.String:
                continue
            result = result.with_columns(
                pl.when(pl.col(col).is_in(nulls)).then(pl.lit(None, dtype=pl.String)).otherwise(pl.col(col)).alias(col)
            )
        return result

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "fields": self.fields, "null_values": list(self.null_values)}


class NormalizeBoolean(NormalizationRule):
    def __init__(
        self,
        field: str,
        *,
        mapping: dict[Any, bool] | None = None,
        true: tuple[str, ...] = _DEFAULT_TRUE,
        false: tuple[str, ...] = _DEFAULT_FALSE,
    ) -> None:
        self.field = field
        if mapping is None:
            mapping = {}
            mapping.update({v: True for v in true})
            mapping.update({v: False for v in false})
        self.mapping = mapping

    def validate(self) -> None:
        if not self.mapping:
            raise RuleConfigurationError("NormalizeBoolean: mapping must not be empty")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"NormalizeBoolean: column {self.field!r} not found")
        table = {str(k).lower(): v for k, v in self.mapping.items()}
        lookup = pl.col(self.field).cast(pl.String).str.to_lowercase().str.strip_chars()
        mapped = lookup.replace_strict(table, default=pl.lit(None))
        return data.with_columns(mapped.cast(pl.Boolean).alias(self.field))

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "mapping": self.mapping}


class NormalizeDate(NormalizationRule):
    def __init__(self, field: str, formats: tuple[str, ...] | None = None, *, errors: str = "null") -> None:
        self.field = field
        self.formats = tuple(formats) if formats else _DEFAULT_DATE_FORMATS
        self.errors = errors
        self.validate()

    def validate(self) -> None:
        if not self.formats:
            raise RuleConfigurationError("NormalizeDate: formats must not be empty")
        if self.errors not in ("null", "raise"):
            raise RuleConfigurationError(f"NormalizeDate: invalid errors mode {self.errors!r}")

    def _dtype(self) -> Any:
        has_time = any(any(part in fmt for part in ("%H", "%M", "%S")) for fmt in self.formats)
        return pl.Datetime if has_time else pl.Date

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"NormalizeDate: column {self.field!r} not found")
        dtype = self._dtype()
        if data[self.field].dtype in (pl.Date, pl.Datetime):
            return data

        parsed = pl.coalesce(*[_str_to_datetime(self.field, fmt) for fmt in self.formats]).cast(dtype)

        if self.errors == "raise":
            failures = data.filter(pl.col(self.field).is_not_null() & parsed.is_null()).height
            if failures:
                raise TransformationError(f"NormalizeDate: {failures} unparseable value(s) in column {self.field!r}")

        return data.with_columns(parsed.alias(self.field))

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "formats": list(self.formats), "errors": self.errors}


def _str_to_datetime(col: str, fmt: str) -> pl.Expr:
    return pl.col(col).str.to_datetime(fmt, strict=False)


class NormalizeCountry(NormalizationRule):
    def __init__(self, field: str, extra_aliases: dict[str, str] | None = None) -> None:
        self.field = field
        from hermes.resources.countries import country_aliases

        self.aliases = dict(country_aliases())
        if extra_aliases:
            for alias, code in extra_aliases.items():
                self.aliases[alias.lower()] = code
        self.validate()

    def validate(self) -> None:
        if not self.aliases:
            raise RuleConfigurationError("NormalizeCountry: no country mapping available")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"NormalizeCountry: column {self.field!r} not found")
        return _map_column(data, self.field, self.aliases, case_insensitive=True)

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "aliases": len(self.aliases)}


class NormalizeCurrency(NormalizationRule):
    def __init__(self, field: str, extra_aliases: dict[str, str] | None = None) -> None:
        self.field = field
        self.aliases = dict(_CURRENCY_ALIASES)
        if extra_aliases:
            for alias, code in extra_aliases.items():
                self.aliases[alias.lower()] = code

    def validate(self) -> None:
        if not self.aliases:
            raise RuleConfigurationError("NormalizeCurrency: no currency mapping available")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"NormalizeCurrency: column {self.field!r} not found")
        return _map_column(data, self.field, self.aliases, case_insensitive=True)

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "aliases": len(self.aliases)}


class NormalizeUnit(NormalizationRule):
    def __init__(self, field: str, extra_aliases: dict[str, str] | None = None) -> None:
        self.field = field
        self.aliases = dict(_UNIT_SYMBOLS)
        if extra_aliases:
            for alias, symbol in extra_aliases.items():
                self.aliases[alias.lower()] = symbol
        self.validate()

    def validate(self) -> None:
        if not self.aliases:
            raise RuleConfigurationError("NormalizeUnit: no unit mapping available")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"NormalizeUnit: column {self.field!r} not found")
        return _map_column(data, self.field, self.aliases, case_insensitive=True)

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "aliases": len(self.aliases)}


class ConvertUnit(NormalizationRule):
    def __init__(
        self,
        field: str,
        from_unit: str,
        to_unit: str,
        factors: dict[str, float] | None = None,
    ) -> None:
        self.field = field
        self.from_unit = from_unit
        self.to_unit = to_unit
        self._factors = dict(factors) if factors else dict(_UNIT_FACTORS)
        self.validate()

    def _canonical(self, unit: str) -> str:
        return _UNIT_SYMBOLS.get(unit.lower(), unit.lower())

    def validate(self) -> None:
        src = self._canonical(self.from_unit)
        dst = self._canonical(self.to_unit)
        if src not in self._factors:
            raise RuleConfigurationError(f"ConvertUnit: unknown from_unit {self.from_unit!r}")
        if dst not in self._factors:
            raise RuleConfigurationError(f"ConvertUnit: unknown to_unit {self.to_unit!r}")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"ConvertUnit: column {self.field!r} not found")
        factor = self._factors[self._canonical(self.from_unit)] / self._factors[self._canonical(self.to_unit)]
        if factor == 1.0:
            return data
        return data.with_columns((pl.col(self.field).cast(pl.Float64) * factor).alias(self.field))

    def describe(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "field": self.field,
            "from_unit": self._canonical(self.from_unit),
            "to_unit": self._canonical(self.to_unit),
        }


class NormalizeIdentifier(NormalizationRule):
    def __init__(
        self,
        field: str,
        *,
        case: Literal["upper", "lower", None] = "upper",
        strip: bool = True,
        remove: str | tuple[str, ...] = (),
    ) -> None:
        self.field = field
        self.case = case
        self.strip = strip
        self.remove = tuple(remove) if isinstance(remove, tuple) else tuple(remove)

    def validate(self) -> None:
        if self.case not in (None, "upper", "lower"):
            raise RuleConfigurationError(f"NormalizeIdentifier: invalid case {self.case!r}")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"NormalizeIdentifier: column {self.field!r} not found")
        e: pl.Expr = pl.col(self.field).cast(pl.String)
        if self.strip:
            e = e.str.strip_chars()
        for ch in self.remove:
            e = e.str.replace_all(re.escape(ch), "")
        if self.case == "upper":
            e = e.str.to_uppercase()
        elif self.case == "lower":
            e = e.str.to_lowercase()
        return data.with_columns(e.alias(self.field))

    def describe(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "field": self.field,
            "case": self.case,
            "strip": self.strip,
            "remove": list(self.remove),
        }


class NormalizeName(NormalizationRule):
    def __init__(
        self,
        field: str,
        *,
        strip: bool = True,
        collapse_whitespace: bool = True,
        unicode_norm: str | None = "NFKC",
        case: Literal["lower", "upper", "title", None] = None,
        remove_chars: str = "",
    ) -> None:
        self.field = field
        self.strip = strip
        self.collapse = collapse_whitespace
        self.unicode_norm = unicode_norm
        self.case = case
        self.remove_chars = remove_chars

    def validate(self) -> None:
        if self.case not in (None, "lower", "upper", "title"):
            raise RuleConfigurationError(f"NormalizeName: invalid case {self.case!r}")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"NormalizeName: column {self.field!r} not found")
        e = _string_expr(
            self.field,
            strip=self.strip,
            collapse=self.collapse,
            unicode_norm=self.unicode_norm,
            case=self.case,
        )
        if self.remove_chars:
            chars = "".join(re.escape(c) for c in self.remove_chars)
            e = e.str.replace_all(f"[{chars}]", "")
        return data.with_columns(e.alias(self.field))

    def describe(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "field": self.field,
            "strip": self.strip,
            "collapse_whitespace": self.collapse,
            "unicode": self.unicode_norm,
            "case": self.case,
            "remove_chars": self.remove_chars,
        }


class MapValue(NormalizationRule):
    def __init__(self, field: str, mapping: dict[Any, Any], *, case_insensitive: bool = False) -> None:
        self.field = field
        self.mapping = dict(mapping)
        self.case_insensitive = case_insensitive
        self.validate()

    def validate(self) -> None:
        if not self.mapping:
            raise RuleConfigurationError("MapValue: mapping must not be empty")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"MapValue: column {self.field!r} not found")
        return _map_column(data, self.field, self.mapping, case_insensitive=self.case_insensitive)

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "mapping": self.mapping}


class MapConcept(MapValue):
    pass


def _parse_period(value: str) -> str | None:
    v = value.strip()
    if not v:
        return None
    m = _PERIOD_RE.fullmatch(v)
    if not m:
        return None
    prefix_leading, year, qtr, prefix_swapped, qtr_swapped, year_swapped = m.groups()

    if prefix_swapped:
        order = prefix_swapped.upper()
        if order == "Q":
            return f"{year_swapped}Q{qtr_swapped}"
        if order == "FQ":
            return f"FQ{year_swapped}Q{qtr_swapped}"
        return f"FY{year_swapped}"

    prefix = (prefix_leading or "").upper()
    if prefix == "Q":
        return f"{year}{'Q' + qtr if qtr else ''}"
    if prefix == "FQ":
        return f"FQ{year}{'Q' + qtr if qtr else ''}"
    if prefix == "FY":
        return f"FY{year}"
    return f"{year}{'Q' + qtr if qtr else ''}"


class ParsePeriod(NormalizationRule):
    def __init__(self, field: str) -> None:
        self.field = field

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"ParsePeriod: column {self.field!r} not found")
        src = pl.col(self.field).cast(pl.String)
        parsed = src.map_elements(_parse_period, return_dtype=pl.String)
        return data.with_columns(pl.coalesce(parsed, src).alias(self.field))

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field}


class StripCharacters(NormalizationRule):
    def __init__(self, field: str, characters: str) -> None:
        if not characters:
            raise RuleConfigurationError("StripCharacters: characters must not be empty")
        self.field = field
        self.characters = characters
        self.validate()

    def validate(self) -> None:
        if not self.characters:
            raise RuleConfigurationError("StripCharacters: characters must not be empty")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"StripCharacters: column {self.field!r} not found")
        pattern = "".join(re.escape(c) for c in self.characters)
        cleaned = pl.col(self.field).cast(pl.String).str.replace_all(f"[{pattern}]", "")
        return data.with_columns(cleaned.alias(self.field))

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "characters": self.characters}


class Round(NormalizationRule):
    def __init__(self, field: str, precision: int = 2, *, half_up: bool = False) -> None:
        self.field = field
        self.precision = precision
        self.half_up = half_up
        self.validate()

    def validate(self) -> None:
        if not isinstance(self.precision, int) or self.precision < 0:
            raise RuleConfigurationError(f"Round: precision must be a non-negative integer, got {self.precision!r}")

    def apply(self, data: pl.DataFrame, context: Any = None) -> pl.DataFrame:
        if self.field not in data.columns:
            raise RuleExecutionError(f"Round: column {self.field!r} not found")
        e: pl.Expr = pl.col(self.field).cast(pl.Float64)
        if self.half_up:
            e = e.map_elements(_round_half_up(self.precision), return_dtype=pl.Float64)
        else:
            e = e.round(self.precision)
        return data.with_columns(e.alias(self.field))

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "field": self.field, "precision": self.precision, "half_up": self.half_up}


def _round_half_up(precision: int):
    factor = 10**precision

    def fn(value):
        if value is None:
            return None
        return math.floor(value * factor + 0.5) / factor

    return fn
