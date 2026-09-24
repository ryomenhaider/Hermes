import polars as pl

import hermes as hr
from hermes.core.dataset import Dataset
from hermes.entities.aliases import add_alias, list_aliases, resolve_alias


def test_add_and_resolve_alias():
    assert resolve_alias("NVIDIA") is None
    add_alias("HRM-COMPANY-ABC", "NVIDIA")
    assert resolve_alias("nvidia") == "HRM-COMPANY-ABC"
    assert list_aliases("HRM-COMPANY-ABC") == ["NVIDIA"]


def test_inspect_reports_entity_needs():
    df = pl.DataFrame({"ticker": ["AAPL"], "iso3": ["USA"], "value": [1.0]})
    report = hr.inspect(df)
    assert ("ticker", "company") in report.needs
    assert ("iso3", "country") in report.needs
    assert all(col != "value" for col, _ in report.needs)


def test_resolve_data_adds_entity_id_columns():
    df = pl.DataFrame({"ticker": ["AAPL", "NVDA", "NOTATICKER"], "iso3": ["USA", "DEU", "ZZZ"]})
    ds = Dataset(name="securities", data=df).record("fetch", input_ref="demo")
    out = hr.resolve_data(ds)
    assert out is ds
    resolved = out.to_polars() if hasattr(out, "to_polars") else out
    ids = resolved["ticker_entity_id"].to_list()
    assert ids[0] and ids[1] and ids[0] != ids[1]
    assert ids[2] is None
    iso_ids = resolved["iso3_entity_id"].to_list()
    assert iso_ids[0] and iso_ids[0] != iso_ids[1]
    assert iso_ids[2] is None
    assert ds.lineage.last_operation().operation == "resolve_data"


def test_resolve_data_requires_resolvable_column():
    df = pl.DataFrame({"value": [1.0]})
    try:
        hr.resolve_data(df)
    except Exception as exc:  # noqa: BLE001
        assert "pass keys" in str(exc)
    else:
        raise AssertionError("expected HermesError")


def test_resolve_data_explicit_keys():
    df = pl.DataFrame({"code": ["AAPL"]})
    resolved = hr.resolve_data(df, keys=[("code", "company")])
    assert resolved["code_entity_id"].to_list() == [hr.resolve_company("AAPL").data.id]