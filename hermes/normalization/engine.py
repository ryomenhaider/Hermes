from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from typing import Any

import polars as pl

try:
    import pyarrow as pa
except ImportError:
    pa = None

from hermes.normalization.context import NormalizationContext
from hermes.normalization.errors import NormalizationError, RuleConfigurationError, RuleExecutionError
from hermes.normalization.result import NormalizationResult
from hermes.normalization.rule import NormalizationRule


class NormalizationEngine:

    def __init__(self, rules: list[NormalizationRule] | None = None, context: NormalizationContext | None = None):
        self._rules: list[NormalizationRule] = []
        self.context = context or NormalizationContext()
        if rules:
            self.add_rules(rules)

    def add_rule(self, rule: NormalizationRule) -> NormalizationEngine:
        """_summary_
        Args:
            rule (NormalizationRule): the rule to add to the engine

        Raises:
            RuleConfigurationError: if the rule is not a NormalizationRule or fails validation

        Returns:
            NormalizationEngine: self, to allow for method chaining
        """
        if not isinstance(rule, NormalizationRule):
            raise RuleConfigurationError(f"Expected a NormalizationRule, got {type(rule).__name__}")
        rule.validate()
        self._rules.append(rule)
        return self

    def add_rules(self, rules: Iterable[NormalizationRule]) -> NormalizationEngine:
        for rule in rules:
            self.add_rule(rule)
        return self

    def remove_rule(self, rule: NormalizationRule | str) -> NormalizationEngine:
        target = rule.name if isinstance(rule, NormalizationRule) else rule
        for index, configured in enumerate(self._rules):
            if configured.name == target:
                self._rules.pop(index)
                return self
        raise RuleConfigurationError(f"No rule named {target!r} is configured")

    def clear_rules(self) -> NormalizationEngine:
        self._rules.clear()
        return self

    @property
    def rules(self) -> list[NormalizationRule]:
        return list(self._rules)

    def validate(self) -> None:
        for rule in self._rules:
            rule.validate()

    def describe(self) -> list[dict[str, Any]]:
        return [rule.describe() for rule in self._rules]

    def normalize(self, data: Any, context: NormalizationContext | None = None) -> Any:

        self.validate()
        frame, kind = self._to_frame(data)
        ctx = context or self.context
        for rule in self._rules:
            frame = self._apply(rule, frame, ctx)
        return self._restore(frame, kind)

    def normalize_record(
        self, record: Mapping[str, Any], context: NormalizationContext | None = None
    ) -> dict[str, Any]:

        frame, _ = self._to_frame(record)
        ctx = context or self.context
        for rule in self._rules:
            frame = self._apply(rule, frame, ctx)
        return frame.to_dicts()[0] if frame.height else {}

    def normalize_stream(
        self, records: Iterable[Mapping[str, Any]], context: NormalizationContext | None = None
    ) -> Iterator[dict[str, Any]]:
        for record in records:
            yield self.normalize_record(record, context)

    def normalize_report(self, data: Any, context: NormalizationContext | None = None) -> NormalizationResult:

        self.validate()
        frame, kind = self._to_frame(data)
        ctx = context or self.context
        rule_names: list[str] = []
        changes_total = 0
        errors: list[str] = []
        warnings: list[str] = []

        for rule in self._rules:
            before = frame
            try:
                frame = self._apply(rule, frame, ctx)
            except NormalizationError as exc:
                errors.append(str(exc))
                return NormalizationResult(
                    data=None,
                    success=False,
                    rules=rule_names,
                    changes=changes_total,
                    errors=errors,
                    warnings=warnings,
                )
            rule_names.append(rule.name)
            changes_total += _changed_cells(before, frame)

        return NormalizationResult(
            data=self._restore(frame, kind),
            success=True,
            rules=rule_names,
            changes=changes_total,
            errors=errors,
            warnings=warnings,
        )

    @staticmethod
    def _apply(rule: NormalizationRule, frame: pl.DataFrame, context: NormalizationContext) -> pl.DataFrame:
        try:
            result = rule.apply(frame, context)
        except NormalizationError:
            raise
        except Exception as exc:
            raise RuleExecutionError(f"{rule.name} failed: {exc}") from exc
        if not isinstance(result, pl.DataFrame):
            raise RuleExecutionError(f"{rule.name} did not return a DataFrame")
        return result

    @staticmethod
    def _to_frame(data: Any) -> tuple[pl.DataFrame, str]:
        if isinstance(data, pl.DataFrame):
            return data, "df"
        if isinstance(data, pl.LazyFrame):
            return data.collect(engine='streaming'), "lazy"
        if pa is not None and isinstance(data, pa.Table):
            frame = pl.from_arrow(data)
            if not isinstance(frame, pl.DataFrame):
                raise NormalizationError("Unsupported pyarrow Table conversion")
            return frame, "arrow"
        if isinstance(data, Mapping):
            return pl.DataFrame([dict(data)]), "record"
        if isinstance(data, (list, tuple)):
            return pl.from_dicts([dict(item) for item in data]), "records"
        raise NormalizationError(
            f"Unsupported data type: {type(data).__name__}. "
            "Expected polars DataFrame/LazyFrame, pyarrow Table, or dict/list of dicts."
        )

    @staticmethod
    def _restore(frame: pl.DataFrame, kind: str) -> Any:
        if kind == "df":
            return frame
        if kind == "lazy":
            return frame.lazy()
        if kind == "arrow":
            return frame.to_arrow()
        if kind == "record":
            return frame.to_dicts()[0] if frame.height else {}
        if kind == "records":
            return frame.to_dicts()
        raise NormalizationError(f"Unknown frame kind {kind!r}")


def _changed_cells(before: pl.DataFrame, after: pl.DataFrame) -> int:
    shared = set(before.columns) & set(after.columns)
    total = 0
    for col in shared:
        if before[col].dtype != after[col].dtype:
            total += before.height
            continue
        total += int((before[col] != after[col]).fill_null(False).sum())
    total += max(0, len(after.columns) - len(shared)) * after.height
    total += max(0, len(before.columns) - len(shared)) * before.height
    return total


__all__ = ["NormalizationEngine"]
