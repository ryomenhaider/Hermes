from __future__ import annotations

from pathlib import Path

import polars as pl
import pytest

import hermes as hr
from hermes.core.dataset import Dataset
from hermes.core.errors import ConnectorNotFoundError


def _mock_fetch(connector, monkeypatch, payload):
    class FakeConn:
        pass

    fake = FakeConn()
    fake.fetch = lambda **kwargs: payload
    fake._fetch = lambda **kwargs: payload
    monkeypatch.setattr("hermes.api.acquire._connector", lambda source: fake)
    return fake


def test_fetch_routes_to_connector(monkeypatch):
    payload = "cached-raw"
    _mock_fetch("binance", monkeypatch, payload)
    assert hr.fetch("binance", symbol="BTCUSDT") == "cached-raw"


def test_fetch_raw_bypasses_dataset(monkeypatch):
    payload = {"t": [1, 2, 3]}
    _mock_fetch("finnhub", monkeypatch, payload)
    assert hr.fetch_raw("finnhub", endpoint="quote", symbol="AAPL") == payload


def test_ingest_api_source_wraps_non_dataset(monkeypatch):
    raw = pl.DataFrame({"open": [1.0], "close": [2.0]})
    _mock_fetch("fred", monkeypatch, raw)
    dataset = hr.ingest("fred", series_id="GDPC1")
    assert isinstance(dataset, Dataset)
    assert dataset.data.width == 2


def test_sync_refreshes_with_force(monkeypatch):
    calls: dict = {}

    class FakeConn:
        def _fetch(self, **kwargs):
            return "raw"

        def fetch(self, **kwargs):
            calls.update(kwargs)
            return pl.DataFrame({"x": [1]})

    monkeypatch.setattr("hermes.api.acquire._connector", lambda source: FakeConn())
    hr.sync("fred", series_id="GDPC1")
    assert calls["force"] is True


def test_read_returns_dataset_named_after_file(tmp_path):
    path = tmp_path / "sample.csv"
    path.write_text("a,b\n1,2\n3,4\n")
    dataset = hr.read(str(path))
    assert isinstance(dataset, Dataset)
    assert dataset.name == "sample"
    assert dataset.to_polars().height == 2


def test_ingest_file_source(tmp_path):
    path = tmp_path / "data.json"
    path.write_text('[{"x": 1}, {"x": 2}]')
    dataset = hr.ingest(path)
    assert isinstance(dataset, Dataset)
    assert dataset.name == "data"


def test_unknown_source_raises(monkeypatch):
    monkeypatch.setattr(Path, "exists", lambda self, *a: False, raising=False)
    monkeypatch.setattr("pathlib.Path.exists", lambda self, *a: False)
    with pytest.raises(ConnectorNotFoundError):
        hr.fetch("not-a-source")