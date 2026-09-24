import datetime

import polars as pl
import pytest

try:
    import pyarrow as pa
except ImportError:  # pragma: no cover
    pa = None

from hermes.validation import (
    CardinalityCheck,
    ColumnCheck,
    CompletenessCheck,
    ConstantCheck,
    DateOrderCheck,
    DateRangeCheck,
    DuplicateCheck,
    EnumCheck,
    ForeignKeyCheck,
    FreshnessCheck,
    LengthCheck,
    NotNull,
    NullRateCheck,
    PatternCheck,
    RangeCheck,
    ReferentialCheck,
    RegexCheck,
    RowCountCheck,
    RuleConfigurationError,
    SchemaCheck,
    TypeCheck,
    Unique,
    UniqueCombination,
    ValidationEngine,
    ValidationRule,
    register_pattern,
)
from hermes.validation.errors import RuleExecutionError

D = datetime.date
DT = datetime.datetime


def check(rule, rows, **kwargs):
    return rule.check(pl.DataFrame(rows), **kwargs)


# -- NotNull -----------------------------------------------------------------


def test_notnull_valid():
    r = check(NotNull("a"), [{"a": 1}, {"a": 2}])
    assert r.passed and r.statistics["null_count"] == 0


def test_notnull_invalid():
    r = check(NotNull("a"), [{"a": 1}, {"a": None}])
    assert not r.passed
    assert r.statistics == {"total_count": 2, "null_count": 1, "null_rate": 0.5}
    assert [v.row for v in r.violations] == [1]


def test_notnull_empty():
    r = NotNull("a").check(pl.DataFrame({"a": pl.Series([], dtype=pl.Int64)}))
    assert r.passed and r.statistics["total_count"] == 0


def test_notnull_missing_column_is_execution_error():
    with pytest.raises(RuleExecutionError):
        check(NotNull("nope"), [{"a": 1}], context=None)


# -- Unique ------------------------------------------------------------------


def test_unique_valid():
    r = check(Unique("a"), [{"a": 1}, {"a": 2}, {"a": None}])
    assert r.passed
    assert r.statistics["unique_count"] == 2


def test_unique_invalid():
    r = check(Unique("a"), [{"a": 1}, {"a": 2}, {"a": 2}])
    assert not r.passed
    assert r.statistics["duplicate_count"] == 2
    assert r.statistics["total_count"] == 3


# -- UniqueCombination -------------------------------------------------------


def test_unique_combination():
    rows = [{"c": "PK", "r": 123}, {"c": "PK", "r": 124}, {"c": "US", "r": 123}, {"c": "PK", "r": 123}]
    r = check(UniqueCombination(["c", "r"]), rows)
    assert not r.passed
    assert r.statistics["duplicate_count"] == 2
    assert r.statistics["unique_count"] == 3


def test_unique_combination_passes():
    r = check(UniqueCombination(["a", "b"]), [{"a": 1, "b": 1}, {"a": 1, "b": 2}])
    assert r.passed


# -- TypeCheck ---------------------------------------------------------------


def test_typecheck_valid():
    r = check(TypeCheck("revenue", "float"), [{"revenue": 1.5}, {"revenue": 2.0}])
    assert r.passed
    assert r.statistics["actual_types"] == {"revenue": "Float64"}


def test_typecheck_mismatch():
    r = check(TypeCheck("id", "integer"), [{"id": "x"}])
    assert not r.passed
    assert r.statistics["invalid_count"] == 1


def test_typecheck_dict_form():
    r = check(TypeCheck({"a": "string", "b": "integer"}), [{"a": "x", "b": 1}])
    assert r.passed


def test_typecheck_unsupported_type():
    with pytest.raises(RuleConfigurationError):
        check(TypeCheck("a", "monetary"), [{"a": 1}])


# -- RangeCheck --------------------------------------------------------------


def test_range_valid():
    r = check(RangeCheck("age", min=0, max=120), [{"age": 30}, {"age": 100}])
    assert r.passed
    assert r.statistics["actual_min"] == 30 and r.statistics["actual_max"] == 100


def test_range_invalid():
    r = check(RangeCheck("age", min=0, max=120), [{"age": -5}, {"age": 30}, {"age": 200}])
    assert not r.passed
    assert r.statistics == {
        "min": 0,
        "max": 120,
        "actual_min": -5,
        "actual_max": 200,
        "below_min": 1,
        "above_max": 1,
        "invalid_count": 2,
    }


def test_range_nulls_ignored():
    r = check(RangeCheck("age", min=0), [{"age": None}, {"age": 5}])
    assert r.passed


def test_range_boundary_inclusive():
    r = check(RangeCheck("age", min=0, max=120), [{"age": 0}, {"age": 120}])
    assert r.passed


def test_range_not_numeric_is_error():
    with pytest.raises(RuleExecutionError):
        check(RangeCheck("a", min=0), [{"a": "x"}])


# -- EnumCheck ---------------------------------------------------------------


def test_enum_valid():
    r = check(EnumCheck("status", allowed=["active", "inactive"]), [{"status": "active"}])
    assert r.passed


def test_enum_invalid():
    r = check(
        EnumCheck("status", allowed=["active", "inactive"]),
        [{"status": "bogus"}, {"status": "active"}, {"status": None}],
    )
    assert not r.passed
    assert r.statistics["invalid_count"] == 1
    assert r.statistics["invalid_values"] == ["bogus"]


def test_enum_numeric_allowed():
    r = check(EnumCheck("code", allowed=[1, 2]), [{"code": 3}])
    assert not r.passed


# -- RegexCheck --------------------------------------------------------------


def test_regex_valid():
    r = check(RegexCheck("ticker", r"^[A-Z]{1,5}$"), [{"ticker": "AAPL"}, {"ticker": "MSFT"}])
    assert r.passed


def test_regex_invalid():
    r = check(RegexCheck("ticker", r"^[A-Z]{1,5}$"), [{"ticker": "aapl"}, {"ticker": "AAPL"}])
    assert not r.passed
    assert r.statistics["invalid_values"] == ["aapl"]


# -- LengthCheck -------------------------------------------------------------


def test_length_valid():
    r = check(LengthCheck("ticker", min=1, max=5), [{"ticker": "AAPL"}, {"ticker": "MF"}])
    assert r.passed


def test_length_invalid():
    r = check(LengthCheck("ticker", min=1, max=5), [{"ticker": "TOOLONG"}, {"ticker": ""}])
    assert not r.passed
    assert r.statistics["invalid_count"] == 2
    assert r.statistics["actual_min"] == 0


# -- DateRangeCheck ----------------------------------------------------------


def test_daterange_valid():
    r = check(DateRangeCheck("d", min="2020-01-01", max="2026-12-31"), [{"d": D(2022, 5, 1)}])
    assert r.passed


def test_daterange_invalid():
    rows = [{"d": D(2019, 12, 31)}, {"d": D(2022, 5, 1)}, {"d": D(2027, 1, 1)}]
    r = check(DateRangeCheck("d", min="2020-01-01", max="2026-12-31"), rows)
    assert not r.passed
    assert r.statistics["before_min"] == 1
    assert r.statistics["after_max"] == 1
    assert r.statistics["invalid_count"] == 2


def test_daterange_non_date_column_is_error():
    with pytest.raises(RuleExecutionError):
        check(DateRangeCheck("d", min="2020-01-01"), [{"d": "2022-01-01"}])


def test_daterange_datetime_column():
    rows = [{"d": DT(2021, 1, 1, 12, 30)}]
    r = check(DateRangeCheck("d", min="2020-01-01", max="2026-12-31"), rows)
    assert r.passed


# -- DateOrderCheck ----------------------------------------------------------


def test_dateorder_sequence_valid():
    rows = [{"d": D(2024, 1, 1)}, {"d": D(2024, 1, 1)}, {"d": D(2024, 2, 1)}]
    r = check(DateOrderCheck("d"), rows)
    assert r.passed


def test_dateorder_sequence_invalid():
    rows = [{"d": D(2024, 1, 1)}, {"d": D(2024, 3, 1)}, {"d": D(2024, 2, 1)}]
    r = check(DateOrderCheck("d"), rows)
    assert not r.passed
    assert r.statistics["out_of_order_count"] == 1
    assert r.statistics["first_violation"]["row"] == 2


def test_dateorder_pairwise_valid():
    rows = [{"s": D(2024, 1, 1), "e": D(2024, 1, 2)}, {"s": D(2024, 1, 1), "e": D(2024, 1, 1)}]
    r = check(DateOrderCheck("s", "e"), rows)
    assert r.passed


def test_dateorder_pairwise_invalid():
    rows = [{"s": D(2024, 2, 1), "e": D(2024, 1, 1)}]
    r = check(DateOrderCheck("s", "e"), rows)
    assert not r.passed
    assert r.statistics["invalid_count"] == 1
    assert r.statistics["mode"] == "pairwise"


# -- SchemaCheck -------------------------------------------------------------


def test_schemacheck_valid():
    rows = [{"company_id": "1", "revenue": 1.0}]
    r = check(SchemaCheck({"company_id": "string", "revenue": "float"}), rows)
    assert r.passed


def test_schemacheck_missing_and_mismatch():
    rows = [{"company_id": "1", "revenue": "not-a-number"}]
    r = check(SchemaCheck({"company_id": "string", "revenue": "float"}), rows)
    assert not r.passed
    assert r.statistics["missing_columns"] == []
    assert r.statistics["type_mismatches"][0]["column"] == "revenue"
    assert r.statistics["type_mismatches"][0]["expected"] == "float"


def test_schemacheck_missing_column():
    rows = [{"company_id": "1", "country": "PK"}]
    r = check(SchemaCheck({"company_id": "string", "revenue": "float"}), rows)
    assert r.statistics["missing_columns"] == ["revenue"]


def test_schemacheck_unexpected():
    rows = [{"company_id": "1", "extra": 1}]
    r = check(SchemaCheck({"company_id": "string"}), rows)
    assert not r.passed
    assert r.statistics["unexpected_columns"] == ["extra"]


# -- RowCountCheck -----------------------------------------------------------


def test_rowcount_exact():
    r = check(RowCountCheck(exact=2), [{"a": 1}, {"a": 2}])
    assert r.passed
    assert r.statistics["expected_exact"] == 2


def test_rowcount_minmax():
    r = check(RowCountCheck(min=2, max=5), [{"a": 1}, {"a": 2}, {"a": 3}])
    assert r.passed


def test_rowcount_failure():
    r = check(RowCountCheck(exact=5), [{"a": 1}])
    assert not r.passed
    assert r.statistics["actual_count"] == 1


def test_rowcount_ambiguous_config():
    with pytest.raises(RuleConfigurationError):
        RowCountCheck(min=1, exact=2)


# -- ColumnCheck -------------------------------------------------------------


def test_columncheck_valid():
    r = check(ColumnCheck(required=["a", "b"]), [{"a": 1, "b": 2, "c": 3}])
    assert r.passed


def test_columncheck_missing():
    r = check(ColumnCheck(required=["a", "b"]), [{"a": 1}])
    assert not r.passed
    assert r.statistics["missing_columns"] == ["b"]


def test_columncheck_unexpected_disallowed():
    r = check(ColumnCheck(required=["a"], allow_extra=False), [{"a": 1, "b": 2}])
    assert not r.passed
    assert r.statistics["unexpected_columns"] == ["b"]


# -- NullRateCheck -----------------------------------------------------------


def test_nullrate_valid():
    r = check(NullRateCheck("a", max_rate=0.5), [{"a": 1}, {"a": None}, {"a": None}])
    assert not r.passed


def test_nullrate_passes():
    r = check(NullRateCheck("a", max_rate=0.5), [{"a": 1}, {"a": 2}, {"a": None}])
    assert r.passed
    assert r.statistics["null_rate"] == pytest.approx(1 / 3)


def test_nullrate_bad_rate():
    with pytest.raises(RuleConfigurationError):
        NullRateCheck("a", max_rate=1.5)


# -- DuplicateCheck ----------------------------------------------------------


def test_duplicate_rows():
    r = check(DuplicateCheck(), [{"a": 1, "b": "x"}, {"a": 1, "b": "x"}, {"a": 2, "b": "y"}])
    assert not r.passed
    assert r.statistics["duplicate_row_count"] == 2
    assert r.statistics["duplicate_group_count"] == 1


def test_duplicate_columns_subset():
    r = check(DuplicateCheck(columns=["a"]), [{"a": 1, "b": "x"}, {"a": 1, "b": "z"}])
    assert not r.passed


def test_duplicate_none():
    r = check(DuplicateCheck(), [{"a": 1}, {"a": 2}])
    assert r.passed


# -- FreshnessCheck ----------------------------------------------------------


def test_freshness_ok():
    now = DT(2026, 9, 19, 12, 0)
    r = check(FreshnessCheck("ts", "24h", now=now), [{"ts": now - datetime.timedelta(hours=2)}])
    assert r.passed
    assert r.statistics["allowed_age"] == "24h"


def test_freshness_stale():
    now = DT(2026, 9, 19, 12, 0)
    r = check(FreshnessCheck("ts", "24h", now=now), [{"ts": now - datetime.timedelta(days=3)}])
    assert not r.passed
    assert r.statistics["latest_value"].startswith("2026-09-16")


def test_freshness_from_context():
    now = DT(2026, 9, 19, 12, 0)
    r = FreshnessCheck("ts", "1h").check(pl.DataFrame({"ts": [now - datetime.timedelta(minutes=10)]}), {"now": now})
    assert r.passed


def test_freshness_date_column():
    now = DT(2026, 9, 19, 12, 0)
    r = check(FreshnessCheck("d", "7d", now=now), [{"d": D(2026, 9, 15)}])
    assert r.passed


def test_freshness_non_temporal_is_error():
    with pytest.raises(RuleExecutionError):
        check(FreshnessCheck("a", "1h"), [{"a": 1}], context={})


# -- CompletenessCheck -------------------------------------------------------


def test_completeness_valid():
    rows = [{"a": 1, "b": 2}, {"a": 3, "b": 4}]
    r = check(CompletenessCheck(required=["a", "b"]), rows)
    assert r.passed
    assert r.statistics["complete_count"] == 2


def test_completeness_incomplete():
    rows = [{"a": 1, "b": 2}, {"a": 3, "b": None}]
    r = check(CompletenessCheck(required=["a", "b"]), rows)
    assert not r.passed
    assert r.statistics["incomplete_count"] == 1
    assert r.statistics["completeness_rate"] == 0.5


def test_completeness_min_rate():
    rows = [{"a": 1, "b": 2}, {"a": 3, "b": None}]
    r = check(CompletenessCheck(required=["a", "b"], min_rate=0.5), rows)
    assert r.passed


# -- ReferentialCheck / ForeignKeyCheck --------------------------------------


def test_referential_valid():
    ref = [{"id": 1}, {"id": 2}]
    r = check(ReferentialCheck("a", reference=ref, reference_field="id"), [{"a": 1}, {"a": 2}])
    assert r.passed
    assert r.statistics["matched_count"] == 2


def test_referential_missing():
    ref = [{"id": 1}, {"id": 2}]
    r = check(ReferentialCheck("a", reference=ref, reference_field="id"), [{"a": 1}, {"a": 99}, {"a": None}])
    assert not r.passed
    assert r.statistics["missing_reference_count"] == 1
    assert r.statistics["missing_references"] == [99]
    assert r.statistics["matched_count"] == 1


def test_foreign_key_missing():
    ref = pl.DataFrame({"parent_company_id": [10, 20]})
    r = check(
        ForeignKeyCheck("parent_company_id", reference=ref, reference_column="parent_company_id"),
        [{"parent_company_id": 10}, {"parent_company_id": 40}],
    )
    assert not r.passed
    assert r.statistics["invalid_count"] == 1
    assert r.statistics["missing_keys"] == [40]


def test_referential_dtype_mismatch_is_error():
    ref = [{"id": 1}]
    with pytest.raises(RuleExecutionError):
        check(ReferentialCheck("a", reference=ref, reference_field="id"), [{"a": "1"}])


# -- PatternCheck ------------------------------------------------------------


def test_pattern_check_isin():
    r = check(PatternCheck("isin", pattern="ISIN"), [{"isin": "US0378331005"}])
    assert r.passed


def test_pattern_check_invalid():
    r = check(PatternCheck("isin", pattern="ISIN"), [{"isin": "not-an-isin"}])
    assert not r.passed


def test_pattern_check_email():
    r = check(PatternCheck("email", pattern="email"), [{"email": "a@b.co"}])
    assert r.passed
    r2 = check(PatternCheck("email", pattern="email"), [{"email": "nope"}])
    assert not r2.passed


def test_pattern_register_custom():
    register_pattern("LOWER3", r"^[a-z]{3}$")
    r = check(PatternCheck("code", pattern="LOWER3"), [{"code": "abc"}])
    assert r.passed


def test_pattern_configurable_regex():
    r = check(PatternCheck("code", pattern=r"^[a-z]{3}$"), [{"code": "abc"}])
    assert r.passed


def test_pattern_unknown():
    with pytest.raises(RuleConfigurationError):
        PatternCheck("code", pattern="NO_SUCH_PATTERN(")


# -- ConstantCheck -----------------------------------------------------------


def test_constant_valid():
    r = check(ConstantCheck("source", expected="SEC"), [{"source": "SEC"}, {"source": "SEC"}])
    assert r.passed
    assert r.statistics["unique_count"] == 1


def test_constant_no_expected():
    r = check(ConstantCheck("source"), [{"source": "SEC"}, {"source": "SEC"}])
    assert r.passed
    assert r.statistics["value"] == "SEC"


def test_constant_wrong_expected():
    r = check(ConstantCheck("source", expected="SEC"), [{"source": "FT"}])
    assert not r.passed


def test_constant_not_constant():
    r = check(ConstantCheck("source"), [{"source": "SEC"}, {"source": "FT"}])
    assert not r.passed
    assert r.statistics["unique_count"] == 2


# -- CardinalityCheck --------------------------------------------------------


def test_cardinality_valid():
    r = check(CardinalityCheck("country", min=1, max=3), [{"country": "PK"}, {"country": "US"}, {"country": "PK"}])
    assert r.passed
    assert r.statistics["unique_count"] == 2


def test_cardinality_too_many():
    r = check(CardinalityCheck("country", min=1, max=2), [{"country": "PK"}, {"country": "US"}, {"country": "DE"}])
    assert not r.passed


def test_cardinality_empty_column():
    r = check(CardinalityCheck("a", min=0, max=5), [{"a": None}, {"a": None}])
    assert r.passed
    assert r.statistics["unique_count"] == 0


# -- Engine ------------------------------------------------------------------


def test_engine_rules_run_in_order_on_same_data():
    data = pl.DataFrame({"a": ["x", "x", None], "b": [1, 2, 3]})
    result = ValidationEngine([NotNull("a"), Unique("b"), Unique("a")]).validate(data)
    assert [r.rule for r in result.results] == ["NotNull", "Unique", "Unique"]
    assert not result.passed


def test_engine_records_input():
    result = ValidationEngine([NotNull("a")]).validate([{"a": 1}, {"a": None}])
    assert not result.passed
    assert result.success


def test_engine_lazy_and_arrow_input():
    data = pl.DataFrame({"a": [1, 2]})
    lazy = ValidationEngine([RangeCheck("a", min=0)]).validate(data.lazy())
    arrow = ValidationEngine([RangeCheck("a", min=0)]).validate(data.to_arrow())
    assert lazy.passed and arrow.passed


def test_engine_missing_column_is_engine_error():
    result = ValidationEngine([NotNull("nope")]).validate([{"a": 1}])
    assert not result.success
    assert not result.passed
    assert result.errors and result.results == []


def test_engine_some_fail_some_ok():
    data = pl.DataFrame({"a": [1, 2], "b": [3, None]})
    result = ValidationEngine([RangeCheck("a", min=0), NotNull("b")]).validate(data)
    assert result.success
    assert not result.passed
    assert len(result.results) == 2


def test_engine_all_pass():
    data = pl.DataFrame({"a": [1, 2], "b": [3, 4]})
    result = ValidationEngine([NotNull("a"), NotNull("b")]).validate(data)
    assert result.success and result.passed
    assert bool(result)


def test_engine_bad_config_raises():
    with pytest.raises(RuleConfigurationError):
        ValidationEngine([RangeCheck("a")])


def test_engine_remove_clear_add():
    engine = ValidationEngine([NotNull("a"), NotNull("b")])
    assert len(engine.rules) == 2
    engine.remove_rule("NotNull")
    assert len(engine.rules) == 1
    engine.add_rule(NotNull("c"))
    assert len(engine.rules) == 2
    engine.clear_rules()
    assert engine.rules == []


def test_engine_unsupported_input():
    from hermes.validation.errors import ValidationError

    with pytest.raises(ValidationError):
        ValidationEngine().validate(123)


# -- public hr.validate ------------------------------------------------------


def test_hr_validate_intro_example():
    data = [
        {"company_name": "Apple", "company_id": 1, "revenue": 10.5},
        {"company_name": None, "company_id": 2, "revenue": 20.0},
    ]
    result = hr_validate(
        data,
        [NotNull("company_name"), Unique("company_id"), TypeCheck("revenue", "float"), RangeCheck("revenue", min=0)],
    )
    assert result.success
    assert not result.passed
    assert [r.passed for r in result.results] == [False, True, True, True]


def test_to_dict_and_summary():
    data = [{"a": None}]
    result = hr_validate(data, [NotNull("a")])
    payload = result.to_dict()
    assert payload["passed"] is False and payload["success"] is True
    assert payload["results"][0]["rule"] == "NotNull"
    assert "summary" in dir(result)
    assert "FAILED" in result.summary()
    all_pass = hr_validate([{"a": 1}], [NotNull("a")])
    assert "Validation PASSED" in all_pass.summary()


def test_validation_does_not_mutate_input():
    data = pl.DataFrame({"a": [1, 1, None], "b": ["x", "x", "y"]})
    before = data.clone()
    ValidationEngine([NotNull("a"), Unique("a"), RangeCheck("b" if False else "a", min=0)]).validate(data)
    assert data.equals(before)
    records = [{"a": None}]
    hr_validate(records, [NotNull("a")])
    assert records == [{"a": None}]


def hr_validate(data, rules):
    import hermes as hr

    return hr.validate(data, rules=rules)


def test_hr_validate_returns_validationresult():
    import hermes as hr

    result = hr.validate([{"a": 1}], rules=[NotNull("a")])
    assert type(result).__name__ == "ValidationResult"


def test_custom_rule():
    class AllEven(ValidationRule):
        def check(self, data, context=None):
            from hermes.validation.result import RuleResult

            bad = int(data.filter(pl.col("a").is_not_null() & (pl.col("a") % 2 != 0)).height)
            return RuleResult(rule=self.name, passed=bad == 0, statistics={"odd_count": bad}, message="")

    import hermes as hr

    result = hr.validate([{"a": 2}, {"a": 4}], rules=[AllEven()])
    assert result.passed
    result2 = hr.validate([{"a": 3}], rules=[AllEven()])
    assert not result2.passed

def test_hr_validate_with_canonical_schema():
    import hermes as hr

    frame = pl.DataFrame(
        {"entity_id": ["HRM-COUNTRY-ABC"], "date": ["2024-01-01"], "indicator": ["CPI"], "value": [3.5]}
    )
    result = hr.validate(frame, schema="economic.observation")
    assert not result.passed  # missing frequency/unit/source columns
    assert "SchemaCheck" in {r.rule for r in result.results}


def test_hr_validate_with_schema_passes_on_conforming_frame():
    import hermes as hr

    frame = pl.DataFrame(
        {
            "entity_id": ["HRM-COUNTRY-ABC"],
            "date": [datetime.datetime(2024, 1, 1)],
            "indicator": ["CPI"],
            "value": [3.5],
            "unit": ["score"],
            "frequency": ["A"],
            "source": ["test"],
        }
    )
    result = hr.validate(frame, schema="economic.observation")
    assert result.passed

    bad = hr.validate(frame.drop("source"), schema="economic.observation")
    assert not bad.passed
