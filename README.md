# Hermes

### The Data Engine for Python

**Profile. Normalize. Validate. Understand. Build on it. Know where it came from.**

Hermes is a **source-available** (not OSI "open source") Python-native data engine for turning
messy external and existing datasets into clean, profiled, well-understood data — with the story
of *where that data came from* kept alongside it.

It is not another dataframe library. Hermes is the **pipeline layer** around your existing stack
(Polars, PyArrow, DuckDB, Parquet): it brings data in, understands it, cleans and validates it, and
makes it ready for analysis and machine learning.

> **Status: Alpha.** This project is under active development. Everything in **Implemented**
> below actually runs; everything else is explicitly marked **In Development** and tracked in the
> roadmap. See [License](#license): Hermes is available under Elastic License 2.0.

---

## Quick Start

```bash
pip install hermes-plt
```

```python
import hermes as hr
import polars as pl

df = pl.read_csv("gdp.csv")

# Full statistical profile: types, nulls, uniques, ranges, means, distributions
report = hr.profile(df)
print("rows:", report.row_count, "· columns:", report.column_count)
print("date range:", report.date_range)
print("duplicates:", report.quality.duplicate_count)
for col in report.columns[:3]:
    print(col.name, "|", col.dtype, "| nulls:", col.null_count, "| unique:", col.unique_count)

# Quick glance without a full scan
info = hr.inspect(df)
print("rows:", info.row_count, "· columns:", info.column_count)
print("types:", info.columns)

# You can also profile straight from a file
hr.profile(path="gdp.csv")

# Wrap your data in the Hermes Dataset
ds = hr.Dataset(name="gdp", data_ref="gdp.csv", data=df)
ds.profile()
ds.inspect()

# Interoperate with your stack
polars_df = ds.to_polars()  # polars.DataFrame
arrow_tbl = ds.to_arrow()  # pyarrow.Table
pandas_df = ds.to_pandas()  # pandas.DataFrame

# Persist it (writes out/gdp.parquet)
ds.save("out", format="parquet")  # parquet / csv / json
csv_bytes = ds.export("csv")  # raw bytes for your own storage
```

```bash
# The CLI (Rust-backed) currently ships fetch / inspect / dataset / entity
hermes --help
```

---

## Implemented Today

| Capability | Notes |
| --- | --- |
| `hr.profile(df / path)` | Column-by-column stats: dtype, nulls, unique values, min/max, mean, median, std, top values; plus completeness, duplicate and anomaly counts, date range, frequency |
| `hr.inspect(df)` | Fast glance: row/column counts and column types |
| `hr.get_freqs`, `hr.date_ranges`, `hr.anomaly_count` | Frequency detection, temporal range detection, IQR anomaly counts |
| `hr.Dataset` | The Hermes core object (see below) |
| `Dataset.load()`, `.inspect()`, `.profile()` | Load from parquet/csv/json/jsonl/xml and analyze |
| `Dataset.to_polars()/to_arrow()/to_pandas()` | Interchange with the Python data stack |
| `Dataset.save()` / `.export()` | Persist (parquet/csv/json) or export to another system |
| `Dataset.metadata_info/ provenance_info / lineage_info / schema_info` | The beginning of Hermes' provenance story |
| `hr.parse()` / `hr.normalize()` / `hr.validate()` | Parsing engine (csv/json/jsonl/parquet/xml) plus 17 normalization and 22 validation rules |
| Storage: `hr.save` / `hr.load` / `hr.exists` / `hr.delete` / `hr.list_datasets` / `hr.storage_info` | Filesystem backend persisting Dataset + metadata as Parquet or IPC, with load-time integrity checks and `StorageInfo` (records, columns, created/modified) |
| Credentials | `hr.set_cred()/get_cred()/has_cred()/list_creds()/delete_cred()` persisted to `~/.hermes-plt/credentials.json` |
| Scheduler | `@hermes.core.scheduler.schedule` cron/interval jobs |
| Error taxonomy | `HermesError`, `ParseError`, `SchemaError`, `NormalizationError`, `ValidationError`, `StorageError`, `QueryError`, `AcquisitionError` and more |
| CLI | `hermes fetch|inspect|profile|entity|dataset` wired to the data API |
| Connectors (10, experimental) | Binance, Finnhub, FRED, IMF, SEC EDGAR, World Bank, YFinance, OpenSanctions, GDELT (stub), public datasets — all ported onto one `BaseConnector` contract that reuses the acquisition engine (retry / rate-limit / auth handling), and applies normalization, validation and provenance to every source |
| Tests | 362 unit tests covering connectors, scheduler, parsing, normalization, validation, entities, schemas, storage (incl. IPC + integrity), catalog, CLI, and the data API |

### The Dataset object

`Dataset` is the center of Hermes. It holds your data and its metadata together, so a dataset is
never just a file — it is a file **plus its story**:

```python
ds = hr.Dataset(name="gdp", data_ref="gs/imports-1985-2024.csv", data=df)
ds.profile()
ds.schema_info()  # schema reference
ds.lineage_info()  # steps that produced the data
ds.provenance_info()  # where the data came from
```

Over the coming releases, provenance, lineage, validation and versioning will be captured
**automatically** at every stage, so the Dataset's story is trustworthy by construction.

---

## In Development

The core value proposition is being built under a strict, code-first roadmap. The single source
of truth — architecture, subsystem spec, engineering guide, roadmap and strategy — is
[`docs/hermes.md`](docs/hermes.md).

| Stage | What ships |
| --- | --- |
| **Phase 1 — Core foundation** | Full dataset lifecycle: `parse → normalize → validate → profile → Dataset → save → query → export`; automatic provenance & lineage capture; dataset catalog |
| **Phase 2 — Data contracts** | Versioned schema registry with 7 canonical schemas (economic, financial, market, geopolitical, security, entity, document); normalization engine; validation engine; entity resolution (countries, companies, aliases) |
| **Phase 3 — Data in** | Acquisition engine (retry, rate limiting, pagination, sync state); parser engine for CSV / JSON / XML / Parquet; public `fetch / ingest / read` API |
| **Phase 4 — Connectors** | Connector registry + canonical-schema output for the 10 ported connectors (all already share one `BaseConnector` contract with provenance, normalization and validation on every source) |
| **Phase 5 — Scale** | DuckDB query engine, dataset versioning / snapshots / diff, export matrix, benchmarks at 10–100M rows |

The pipeline we are building:

```text
CSV / JSON / XML / Parquet / API
    ↓  fetch/ingest → parse → normalize → validate → metadata + provenance + lineage
                        ↓
                    Canonical Dataset
                        ↓
        store → query → version → export → features
```

---

## Design Principles

- **Local first.** `pip install hermes-plt` and start. Local files, local storage, DuckDB, Parquet,
  Polars — no cloud account, no hosted service, no proprietary storage required.
- **Interoperable, not replaceable.** Hermes sits *between* data sources and your models, and works
  *with* Pandas, Polars, PyArrow, DuckDB and the rest. It does not try to be one of them.
- **One auditable object.** A `Dataset` should carry its data and its complete story — schema,
  metadata, provenance, lineage, version — so you never hold a disconnected file again.
- **Honest by default.** What is built is documented as built; what is planned is documented as
  planned.

---

## Roadmap

The current roadmap is kept in a single document, because the repository *is* the plan:

- **[`docs/hermes.md`](docs/hermes.md)** — what Hermes is, the data lifecycle, architecture,
  the subsystem engineering checklist (the tracked tasks), team & ownership, phased roadmap,
  and strategy/licensing.

---

## Contributing

Hermes is source-available and built for the community. Contributions are welcome in: connectors,
parsers, normalizers, validators, profilers, storage backends, query integrations, documentation,
testing, and performance.

Before contributing: read [`docs/hermes.md`](docs/hermes.md) for architecture, ownership and what is
in flight, and open an issue or PR.

---

## License

Hermes is **source-available** under the **Elastic License 2.0 (ELv2)** — the same license family
used by Elasticsearch and Couchbase infrastructure. This is **not** an OSI-approved "open source"
license; it is a deliberate choice:

- **You may** read, use, modify, fork and redistribute Hermes freely, including for internal
  commercial use.
- **You may not** offer Hermes to third parties as a **hosted or managed service** (a "cloud
  Hermes"). Hosting Hermes for third parties is a Hermes Enterprise privilege.
- **You may not** strip the notices, remove license-key functionality, or use the trademarks.

Companies and products that need to embed or host Hermes commercially can obtain a
**Hermes Enterprise** license (support, SLAs, enterprise features, managed-hosting rights) from the
copyright holders.

Full terms: **[LICENSE.md](LICENSE.md)**.

---

**Bring the data in. Make it usable. Know where it came from. Build on it.**