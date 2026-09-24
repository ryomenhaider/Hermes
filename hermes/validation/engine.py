from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

import polars as pl

try:
    import pyarrow as pa
except ImportError:
    pa = None

from hermes.validation.context import ValidationContext
from hermes.validation.errors import RuleConfigurationError, ValidationError
from hermes.validation.result import RuleResult, ValidationResult
from hermes.validation.rule import ValidationRule


class ValidationEngine:
    def __init__(self, rules: list[ValidationRule] | None = None, context: ValidationContext | None = None):
        self._rules: list[ValidationRule] = []
        self.context = context or ValidationContext()
        if rules:
            self.add_rules(rules)

    def add_rule(self, rule: ValidationRule) -> ValidationEngine:
        if not isinstance(rule, ValidationRule):
            raise RuleConfigurationError(f"Expected a ValidationRule, got {type(rule).__name__}")
        rule.validate()
        self._rules.append(rule)
        return self

    def add_rules(self, rules: Iterable[ValidationRule]) -> ValidationEngine:
        for rule in rules:
            self.add_rule(rule)
        return self

    def remove_rule(self, rule: ValidationRule | str) -> ValidationEngine:
        target = rule.name if isinstance(rule, ValidationRule) else rule
        for index, configured in enumerate(self._rules):
            if configured.name == target:
                self._rules.pop(index)
                return self
        raise RuleConfigurationError(f"No rule named {target!r} is configured")

    def clear_rules(self) -> ValidationEngine:
        self._rules.clear()
        return self

    @property
    def rules(self) -> list[ValidationRule]:
        return list(self._rules)

    def validate(self, data: Any, context: ValidationContext | None = None) -> ValidationResult:
        frame = self._to_frame(data)
        ctx = context or self.context
        results: list[RuleResult] = []
        errors: list[str] = []
        warnings: list[str] = []

        for rule in self._rules:
            try:
                result = rule.check(frame, ctx)
            except ValidationError as exc:
                errors.append(f"{rule.name}: {exc}")
                continue
            except Exception as exc:
                errors.append(f"{rule.name}: {exc}")
                continue
            results.append(result)
            warnings.extend(result.warnings)

        success = not errors
        passed = success and all(r.passed for r in results)
        return ValidationResult(success=success, passed=passed, results=results, errors=errors, warnings=warnings)

    def describe(self) -> list[dict[str, Any]]:
        return [rule.describe() for rule in self._rules]

    @staticmethod
    def _to_frame(data: Any) -> pl.DataFrame:
        if isinstance(data, pl.DataFrame):
            return data
        if isinstance(data, pl.LazyFrame):
            return data.collect(engine='streaming')
        if pa is not None and isinstance(data, pa.Table):
            return pl.DataFrame(pl.from_arrow(data))
        if isinstance(data, Mapping):
            return pl.DataFrame([dict(data)])
        if isinstance(data, (list, tuple)):
            return pl.from_dicts([dict(item) for item in data])
        raise ValidationError(
            f"Unsupported data type: {type(data).__name__}. "
            "Expected polars DataFrame/LazyFrame, pyarrow Table, or dict/list of dicts."
        )


def validate(
    data: Any,
    rules: list[ValidationRule] | None = None,
    context: ValidationContext | None = None,
) -> ValidationResult:

    return ValidationEngine(rules=rules or [], context=context).validate(data, context)


__all__ = ["ValidationEngine", "validate"]
