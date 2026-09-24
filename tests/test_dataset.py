from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import polars as pl

import hermes as hr
from hermes.connectors.world_bank import World_bank
from hermes.core.dataset import Dataset
from hermes.normalization import NormalizeDate
from hermes.validation import NotNull


def _write_csv(path, rows: str) -> None:
    path.write_text(rows)


def _mock_client(client_cls, payload):
    client = MagicMock()
    client.get = MagicMock(return_value=payload)
    client_cls.return_value.__enter__.return_value = client


class TestDatasetOps:
    def test_load_records_lineage_and_version(self, tmp_path):
        p = tmp_path / "data.csv"
        _write_csv(p, "date,value\n2023-01-01,1.5\n")
        ds = Dataset(name="demo", data_ref=str(p))
        data = ds.load()
        assert isinstance(data, pl.LazyFrame)
        assert ds.lineage.last_operation().operation == "load"
        assert ds.data_version is not None

    def test_hr_parse_raw_returns_dataset(self, tmp_path):
        p = tmp_path / "data.csv"
        _write_csv(p, "date,value\n2023-01-01,1.5\n")
        ds = hr.parse(str(p))
        assert isinstance(ds, Dataset)
        assert ds.name == "data"
        assert ds.lineage.last_operation().operation == "parse"
        assert ds.data_version is not None
        assert isinstance(ds.data, pl.LazyFrame)

    def test_hr_parse_dataset_mutates_in_place(self, tmp_path):
        p = tmp_path / "data.csv"
        _write_csv(p, "date,value\n2023-01-01,1.5\n")
        ds = Dataset(name="demo", data_ref=str(p))
        out = hr.parse(ds)
        assert out is ds
        assert ds.lineage.last_operation().operation == "parse"
        assert isinstance(ds.data, pl.LazyFrame)

    def test_hr_normalize_mutates_and_records(self):
        df = pl.DataFrame({"date": ["2023-01-01", "2024-06-15"], "value": [1.5, 2.5]})
        ds = Dataset(name="demo", data=df).record("fetch", input_ref="fred")
        before = ds.data_version.content_hash
        out = hr.normalize(ds, rules=[NormalizeDate("date")])
        assert out is ds
        assert ds.lineage.last_operation().operation == "normalize"
        assert ds.lineage.last_operation().params["report"] is False
        assert ds.data_version.content_hash != before

    def test_hr_validate_records_but_does_not_bump_version(self):
        df = pl.DataFrame({"value": [1.5, 2.5]})
        ds = Dataset(name="demo", data=df).record("fetch", input_ref="fred")
        v1 = ds.data_version.content_hash
        result = hr.validate(ds, rules=[NotNull("value")])
        assert result.passed
        assert ds.lineage.last_operation().operation == "validate"
        assert ds.lineage.last_operation().params["passed"] is True
        assert ds.data_version.content_hash == v1

    def test_hr_validate_raw_input_unchanged(self):
        result = hr.validate([{"value": 1}, {"value": 2}], rules=[NotNull("value")])
        assert result.passed


class TestLazyPath:
    def test_load_and_parse_are_lazy(self, tmp_path):
        p = tmp_path / "big.parquet"
        pl.DataFrame({"date": pl.Series(["2020-01-01", "2021-01-01"]).str.to_date(), "value": [1.5, 2.5]}).write_parquet(p)

        ds = hr.parse(str(p))
        assert isinstance(ds.data, pl.LazyFrame)
        assert isinstance(ds.to_polars(), pl.DataFrame)
        assert ds.to_lazy() is ds.data

    def test_lazy_profile_and_inspect(self, tmp_path):
        p = tmp_path / "big.parquet"
        pl.DataFrame(
            {"date": pl.Series(["2020-01-01", "2021-01-01"]).str.to_date(), "value": [1.5, 2.5], "cat": ["a", "b"]}
        ).write_parquet(p)

        md = hr.profile(path=p)
        assert md.row_count == 2
        assert md.column_count == 3
        assert md.columns[1].mean == 2.0
        assert md.columns[2].top_values
        assert md.frequency is not None

        ds = Dataset(name="demo", data_ref=str(p))
        ds.load()
        assert ds.inspect().row_count == 2
        assert ds.profile().row_count == 2

    def test_profile_parquet_footer_path(self, tmp_path, monkeypatch):
        import hermes.api.data as api_data

        p = tmp_path / "big.parquet"
        pl.DataFrame(
            {"date": pl.Series(["2020-01-01", "2021-01-01"]).str.to_date(), "value": [1.5, 2.5], "cat": ["a", "b"]}
        ).write_parquet(p)

        md = hr.profile(path=p)
        assert md.deep_stats
        cat = next(c for c in md.columns if c.name == "cat")
        assert cat.min_value == "a" and cat.max_value == "b"

        monkeypatch.setattr(api_data, "_HEAVY_ROWS", 1)
        md_light = hr.profile(path=p)
        assert not md_light.deep_stats
        assert md_light.quality.duplicate_count == 0
        assert md_light.quality.anomaly_count == {}
        assert md_light.row_count == 2
        value = next(c for c in md_light.columns if c.name == "value")
        assert value.mean is not None and value.unique_count == 0 and value.top_values == []

        monkeypatch.setattr(api_data, "_SCAN_BUDGET_BYTES", 1)
        md_noscan = hr.profile(path=p)
        assert md_noscan.columns[1].mean is None

    def test_lazy_normalize_and_validate_round_trip(self, tmp_path):
        p = tmp_path / "big.parquet"
        pl.DataFrame({"date": ["2020-01-01", "2021-01-01"], "value": [1.5, 2.5]}).write_parquet(p)

        ds = hr.parse(str(p))
        out = hr.normalize(ds, rules=[NormalizeDate("date")])
        assert isinstance(out.data, pl.LazyFrame)
        vr = hr.validate(ds, rules=[NotNull("value")])
        assert vr.passed


class TestConnectorWrapsDataset:
    def test_world_bank_fetch_returns_dataset_with_provenance(self):
        wb = World_bank(cache=None)
        mock_response = [
            {"page": 1, "pages": 1, "per_page": 1000, "total": 1},
            [
                {
                    "indicator": {"id": "NY.GDP.MKTP.KD.ZG", "value": "GDP growth"},
                    "countryiso3code": "USA",
                    "date": "2023",
                    "value": 2.5,
                }
            ],
        ]

        with patch("hermes.connectors.base.Client") as client_cls:
            _mock_client(client_cls, payload=mock_response)
            ds = wb.fetch("USA", "NY.GDP.MKTP.KD.ZG")

        assert isinstance(ds, Dataset)
        assert isinstance(ds.data, pl.DataFrame)
        assert ds.provenance.source == "world_bank"
        assert ds.provenance.connector == "world_bank"
        assert ds.provenance.retrieved_at is not None
        assert ds.lineage.last_operation().operation == "fetch"
        assert ds.lineage.last_operation().params["indicator"] == "NY.GDP.MKTP.KD.ZG"
        assert ds.data_version is not None
        assert not ds.is_empty()

    def test_raw_payload_dataset_delegates_container_access(self):
        ds = Dataset(name="binance", data=[{"qty": "1.5"}, {"qty": "3"}]).record(
            "fetch", input_ref="binance", params={"symbol": "BTCUSDT"}
        )
        assert [float(t["qty"]) for t in ds] == [1.5, 3.0]
        assert len(ds) == 2
        assert bool(ds)
        assert ds.lineage.last_operation().operation == "fetch"
