import dataclasses
import datetime
import json

import polars as pl
import pytest

import hermes as hr
from hermes.core.dataset import Dataset
from hermes.core.errors import StorageError
from hermes.core.lineage import LineageStep
from hermes.core.metadata import MetaData
from hermes.core.provenance import Provenance
from hermes.core.versioning import DataVersion
from hermes.storage import (
    DatasetAlreadyExistsError,
    DatasetNotFoundError,
    FilesystemStorage,
    StorageCorruptionError,
    StorageReadError,
    StorageWriteError,
)

try:
    import pyarrow as pa
except ImportError:  # pragma: no cover
    pa = None


@pytest.fixture
def store(tmp_path) -> FilesystemStorage:
    return FilesystemStorage(root=tmp_path / "store")


@pytest.fixture
def hr_store(tmp_path):
    hr.configure(storage_root=str(tmp_path / "store"))
    yield
    hr.configure()


def make_dataset(name: str = "world_bank_gdp", rows: int = 4) -> Dataset:
    df = pl.DataFrame(
        {
            "id": list(range(1, rows + 1)),
            "country": ["US", "DE", "PK", "FR"][:rows],
            "gdp": [12.5, 3.4, 0.4, 2.7][:rows],
            "year": list(range(2019, 2019 + rows)),
        }
    )
    return Dataset(data=df, name=name)


def assert_frame_equal(a: pl.DataFrame, b: pl.DataFrame) -> None:
    assert a.equals(b)


# --- save ---


def test_save_writes_files(store):
    store.save(make_dataset())
    data_dir = store.root / "datasets" / "world_bank_gdp"
    assert (data_dir / "data.parquet").is_file()
    assert (data_dir / "metadata.json").is_file()


def test_save_with_explicit_name(store):
    store.save(make_dataset("original"), name="explicit_name")
    assert store.exists("explicit_name")
    assert not store.exists("original")


def test_save_missing_data_raises(store):
    dataset = Dataset(name="empty")
    with pytest.raises(StorageWriteError):
        store.save(dataset)


def test_save_returns_storage_info(store):
    info = store.save(make_dataset())
    assert info.dataset == "world_bank_gdp"
    assert info.rows == 4
    assert info.columns == 4


# --- load / round trip ---


def test_roundtrip_data_schema_metadata(store):
    dataset = make_dataset()
    dataset.metadata = MetaData(row_count=4, column_count=4, source="World Bank")
    dataset.provenance = Provenance(source="World Bank", connector="world_bank", raw_checksum="abc123")
    dataset.lineage.add_step(LineageStep(operation="parse", input_ref="wb.csv", output_ref=dataset.name))
    dataset.data_version = DataVersion(content_hash="c1", schema_hash="s1")

    store.save(dataset)
    loaded = store.load(dataset.name)

    assert loaded.id == dataset.id
    assert loaded.name == dataset.name
    assert loaded.version == dataset.version
    assert loaded.data_ref is not None and loaded.data_ref.endswith("data.parquet")
    assert_frame_equal(loaded.data, dataset.data)
    assert loaded.data.schema == dataset.data.schema
    assert loaded.metadata == dataset.metadata
    assert loaded.provenance == dataset.provenance
    assert loaded.lineage == dataset.lineage
    assert loaded.data_version is not None
    assert loaded.data_version == dataset.data_version
    assert loaded.schema_ref == dataset.schema_ref


def test_load_missing_raises(store):
    with pytest.raises(DatasetNotFoundError):
        store.load("nope")


# --- exists / delete / list ---


def test_exists(store):
    assert not store.exists("world_bank_gdp")
    store.save(make_dataset())
    assert store.exists("world_bank_gdp")


def test_delete(store):
    store.save(make_dataset())
    assert store.exists("world_bank_gdp")
    store.delete("world_bank_gdp")
    assert not store.exists("world_bank_gdp")
    with pytest.raises(DatasetNotFoundError):
        store.delete("world_bank_gdp")


def test_list(store):
    assert store.list() == []
    for name in ("b", "a", "aa"):
        store.save(make_dataset(name))
    assert store.list() == ["a", "aa", "b"]


# --- storage_info ---


def test_storage_info(store):
    dataset = make_dataset()
    dataset.version = "1.2.3"
    dataset.provenance = Provenance(source="WB")
    store.save(dataset)

    info = store.info("world_bank_gdp")
    assert info.dataset == "world_bank_gdp"
    assert info.format == "parquet"
    assert info.rows == 4
    assert info.columns == 4
    assert info.size > 0
    assert info.version == "1.2.3"
    assert info.source == "WB"
    assert isinstance(info.created, datetime.datetime)
    assert isinstance(info.modified, datetime.datetime)
    dtype_map = {c["name"]: c["dtype"] for c in info.column_schema}
    assert set(dtype_map) == {"id", "country", "gdp", "year"}


def test_storage_info_missing_raises(store):
    with pytest.raises(DatasetNotFoundError):
        store.info("nope")


# --- overwrite ---


def test_overwrite_default_rejects(store):
    store.save(make_dataset())
    with pytest.raises(DatasetAlreadyExistsError):
        store.save(make_dataset())
    assert store.load("world_bank_gdp").data.height == 4


def test_overwrite_explicit_replaces(store):
    store.save(make_dataset(rows=4))
    store.save(make_dataset(rows=2), overwrite=True)
    loaded = store.load("world_bank_gdp")
    assert loaded.data.height == 2
    assert store.info("world_bank_gdp").rows == 2


def test_overwrite_keeps_original_created_time(store):
    store.save(make_dataset())
    original_created = store.info("world_bank_gdp").created
    store.save(make_dataset(rows=2), overwrite=True)
    assert store.info("world_bank_gdp").created == original_created
    assert store.info("world_bank_gdp").modified >= original_created


# --- corrupt / incomplete state ---


def test_corrupt_missing_data_parquet(store):
    store.save(make_dataset())
    (store.root / "datasets" / "world_bank_gdp" / "data.parquet").unlink()
    assert not store.exists("world_bank_gdp")
    with pytest.raises(StorageCorruptionError):
        store.load("world_bank_gdp")


def test_corrupt_missing_metadata(store):
    store.save(make_dataset())
    (store.root / "datasets" / "world_bank_gdp" / "metadata.json").unlink()
    assert not store.exists("world_bank_gdp")
    with pytest.raises(StorageCorruptionError):
        store.load("world_bank_gdp")


def test_corrupt_garbage_parquet(store):
    store.save(make_dataset())
    data_path = store.root / "datasets" / "world_bank_gdp" / "data.parquet"
    data_path.write_bytes(b"this is not parquet data")
    assert store.exists("world_bank_gdp")
    with pytest.raises(StorageReadError):
        store.load("world_bank_gdp")


def test_corrupt_bad_metadata_json(store):
    store.save(make_dataset())
    meta_path = store.root / "datasets" / "world_bank_gdp" / "metadata.json"
    meta_path.write_text("{not valid json", encoding="utf-8")
    with pytest.raises(StorageCorruptionError):
        store.load("world_bank_gdp")
    with pytest.raises(StorageCorruptionError):
        store.info("world_bank_gdp")


# --- atomic writes ---


def test_failed_write_leaves_no_valid_dataset(store, monkeypatch):
    def broken_write(tmp_path: object, **kwargs: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(pl.DataFrame, "write_parquet", broken_write)
    with pytest.raises(StorageWriteError):
        store.save(make_dataset())
    assert not store.exists("world_bank_gdp")
    with pytest.raises(DatasetNotFoundError):
        store.load("world_bank_gdp")


# --- path traversal / safety ---


@pytest.mark.parametrize(
    "bad",
    ["../evil", "..", ".", "", "a/b", "a\\b", "/absolute", "a b", "a\tb", "a:b"],
)
def test_unsafe_names_rejected(store, bad):
    with pytest.raises(StorageError):
        store.exists(bad)
    with pytest.raises(StorageError):
        store.save(make_dataset(), name=bad)


def test_traversal_does_not_escape_root(store, tmp_path):
    with pytest.raises(StorageError):
        store.save(make_dataset(), name="../evil")
    assert not (tmp_path / "evil").exists()
    assert not (store.root.parent / "evil").exists()


# --- input types & large data ---


def test_save_lazyframe(store):
    dataset = Dataset(name="lazy", data=pl.DataFrame({"x": [1, 2, 3]}))
    dataset.data = dataset.data.lazy()
    store.save(dataset)
    loaded = store.load("lazy")
    assert loaded.data["x"].to_list() == [1, 2, 3]
    assert store.info("lazy").rows == 3


@pytest.mark.skipif(pa is None, reason="pyarrow not available")
def test_save_arrow_table(store):
    table = pa.table({"x": [10, 20, 30]})
    dataset = Dataset(name="arrow", data=pl.DataFrame({"x": [10, 20, 30]}))
    dataset.data = table
    store.save(dataset)
    loaded = store.load("arrow")
    assert loaded.data["x"].to_list() == [10, 20, 30]


def test_large_data_no_python_conversion(store, monkeypatch):
    n = 200_000
    tags = ["alpha", "beta", "gamma", "delta"]
    df = pl.DataFrame(
        {
            "id": pl.arange(0, n, eager=True),
            "amount": pl.Series(range(n), dtype=pl.Float64),
            "tag": pl.Series([tags[i % 4] for i in range(n)], dtype=pl.String),
        }
    )
    dataset = Dataset(data=df, name="large")

    def fails(*args: object, **kwargs: object):
        raise AssertionError("storage must not convert columnar data to Python dicts")

    monkeypatch.setattr(pl.DataFrame, "to_dicts", fails)
    store.save(dataset)
    loaded = store.load("large")
    assert loaded.data.height == n
    assert store.info("large").rows == n


# --- public API (hr.*) ---


def test_hr_workflow(hr_store):
    dataset = make_dataset()
    result = hr.save(dataset)
    assert result.is_success()
    assert result.data.rows == 4

    assert hr.list_datasets().data == ["world_bank_gdp"]
    assert hr.exists("world_bank_gdp").data is True

    info = hr.storage_info("world_bank_gdp").data
    assert info.dataset == "world_bank_gdp"
    assert info.rows == 4

    loaded = hr.load("world_bank_gdp").data
    assert isinstance(loaded, Dataset)
    assert_frame_equal(loaded.data, dataset.data)

    assert hr.delete("world_bank_gdp").is_success()
    assert hr.exists("world_bank_gdp").data is False
    missing = hr.load("world_bank_gdp")
    assert missing.is_failure()
    assert missing.errors[0].code == "DatasetNotFoundError"


def test_hr_save_failure_returns_result(hr_store):
    result = hr.save(Dataset(name="dupe"))
    hr.save(make_dataset())
    result = hr.save(make_dataset())
    assert result.is_failure()
    assert result.errors[0].code == "DatasetAlreadyExistsError"


def test_hr_save_overwrite(hr_store):
    hr.save(make_dataset(rows=4))
    result = hr.save(make_dataset(rows=1), overwrite=True)
    assert result.is_success()
    assert hr.load("world_bank_gdp").data.data.height == 1


def test_hr_storage_info_encodeable(hr_store):
    hr.save(make_dataset())
    info = hr.storage_info("world_bank_gdp").data
    json.dumps(dataclasses.asdict(info), default=str)


def test_hr_load_missing_raises(hr_store):
    result = hr.load("missing")
    assert result.is_failure()
    assert result.errors[0].code == "DatasetNotFoundError"


def test_save_load_ipc_roundtrip(store):
    df = pl.DataFrame({"ticker": ["AAPL", "NVDA"], "value": [1.5, 2.5]})
    ds = Dataset(name="ipc_demo", data=df).record("fetch", input_ref="demo")
    info = store.save(ds, format="ipc")
    assert info.format == "ipc"
    assert info.path.endswith("data.ipc")

    loaded = store.load("ipc_demo")
    assert loaded.data.height == 2
    assert loaded.data["ticker"].to_list() == ["AAPL", "NVDA"]
    assert loaded.data_version == ds.data_version
    assert loaded.lineage.last_operation().operation == "fetch"


def test_load_detects_corrupt_shape(store, tmp_path):
    ds = Dataset(name="corruptible", data=pl.DataFrame({"a": [1, 2], "b": [3, 4]}))
    store.save(ds)
    # Truncate the parquet file so the loaded shape differs from stored metadata.
    data_path = store._find_data_path("corruptible")
    bad = pl.DataFrame({"a": [1]})
    bad.write_parquet(data_path)
    with pytest.raises(StorageCorruptionError, match="shape mismatch"):
        store.load("corruptible")


def test_hr_save_format_roundtrip(hr_store):
    ds = Dataset(name="hr_ipc", data=pl.DataFrame({"x": [1]})).record("fetch", input_ref="src")
    saved = hr.save(ds, name="hr_ipc", format="ipc")
    assert saved.is_success()
    assert saved.data.format == "ipc"
    loaded = hr.load("hr_ipc")
    assert loaded.is_success()
    assert loaded.data.to_polars().to_dicts() == [{"x": 1}]
