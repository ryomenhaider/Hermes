import polars as pl

from hermes.core.dataset import Dataset
from hermes.core.provenance import Provenance
from hermes.datasets import DatasetCatalog, DatasetDescriptor, DatasetRegistry
from hermes.storage.filesystem import FilesystemStorage


def test_registry_register_get_search(tmp_path):
    registry = DatasetRegistry()
    alpha = DatasetDescriptor(id="a", name="cpi", description="consumer prices", source="fred")
    beta = DatasetDescriptor(id="b", name="hrs", description="human rights scores", source="public_data")
    registry.register(alpha)
    registry.register(beta)
    assert registry.get("a") is alpha
    assert registry.list_dataset() == [alpha, beta]
    assert {d.id for d in registry.search("price")} == {"a"}
    assert {d.id for d in registry.search("public")} == {"b"}
    try:
        registry.register(DatasetDescriptor(id="a", name="other"))
    except ValueError:
        pass
    else:
        raise AssertionError("expected duplicate registration to raise")


def test_catalog_loads_from_storage(tmp_path):
    store = FilesystemStorage(root=tmp_path)
    ds = Dataset(
        name="catalog_demo",
        data=pl.DataFrame({"x": [1]}),
        provenance=Provenance(source="fred"),
    ).record("fetch", input_ref="fred")
    store.save(ds)

    catalog = DatasetCatalog(storage=store).load()
    names = [d.name for d in catalog.list()]
    assert names == ["catalog_demo"]
    entry = catalog.get("catalog_demo")
    assert entry is not None
    assert entry.source == "fred"
    assert catalog.search("catalog")[0].name == "catalog_demo"