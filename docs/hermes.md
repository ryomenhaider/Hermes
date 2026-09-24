# Hermes

> **One document for architecture, engineering, roadmap, and strategy.**
> This file replaces the previous `docs/**` markdown files (consolidated here) and is the single
> source of truth for the repository. `res/` holds personal scratch docs and is gitignored.

**Status:** Alpha. Source-available under Elastic License 2.0 (ELv2) — see [Part H](#part-h--positioning-licensing--credibility).
Every checkbox in [Part E](#part-e--subsystem-engineering-spec) is tracked here and in the code.

---

## Part A — What Hermes Is

### Elevator

Hermes is a Python-native **data engine** that turns messy external and existing data into clean,
profiled, well-understood, provenance-tracked datasets — and then **serves those datasets for
finance and defense**, resolved by real-world entity.

### The three layers

| Layer | What it is | Customer-visible artifact |
|---|---|---|
| **1. General data engine** | A domain-agnostic data lifecycle: `fetch/ingest → parse → normalize → validate → canonical Dataset`, with metadata, provenance, and lineage attached | `Dataset`, the `hr.*` engine API |
| **2. Special datasets builder** | Curated, versioned canonical datasets (finance & defense) built on the engine | Canonical `Dataset`s in the catalog (`list / search / get`) |
| **3. Data provider** | Entity-centric data access: resolve an entity, then pull its datasets on demand | `hr.resolve_company("AAPL").financials` etc. |

Each layer depends only on the one above it. **Core never knows about finance or defense**;
the entity registry and the provider layer are the only places that know entity types.

### Entity-centric API (the product's face)

```python
import hermes as hr

apple = hr.resolve_company("AAPL")

apple.financials  # SEC/Finnhub financials
apple.market_data  # OHLCV/history via market connectors
apple.fillings  # SEC filings
apple.xxxxx  # extensible per-domain datasets
```

### Entity scope (v1)

- **~100,000 entities**: **companies, countries, and persons** — for **finance and defense**.
- Resolvable by any practical identifier or alias: ticker, CIK, ISIN, LEI, name, ISO-2/ISO-3,
  numeric country code, alias.
- The entity registry is an anchor asset: it turns the engine's outputs into a data product and is
  a competitor-hard moat (see [Part H](#part-h--positioning-licensing--credibility)).

### Product direction

```
1. GENERAL DATA ENGINE   — domain-agnostic lifecycle for ANY source
2. SPECIAL DATASETS       — curated canonical datasets for finance & defense
3. DATA PROVIDER         — entity-centric access to those datasets
```

Other domains (healthcare, trade, energy, climate, geopolitics) are **potentially later**, built the
same way on top of Core. Nothing domain-specific goes into Core.

> **De-scoped from the v1 product identity:** the heavy standalone feature engines (financial
> TA/fundamentals, country-risk pipelines) and the old domain scaffolding were removed. Feature work
> is only considered again after the engine + provider layers are real.

---

## Part B — Data Lifecycle

### The lifecycle

Data must go from **fetching to serving with minimal user effort**, with the complexity kept inside
Hermes:

```text
External Source / File / API
    ↓  fetch() / ingest()
Raw data
    ↓  parse                     → raw becomes easy-to-understand structured records
    ↓  normalize                 → parsed data becomes the Hermes representation
    ↓  validate                  → checked for missing values, outliers, schema conformance
    ↓  metadata + provenance + lineage
Canonical Dataset
    ↓  store → query → version → export
```

### Dataset — the central abstraction

A `Dataset` is a **representation and reference** of data, not a copy of the entire payload:

- It holds a **reference to where the data lives** (e.g. a parquet path / storage location), so data is
  loaded **on demand** rather than held fully in memory from the start.
- It carries the data's complete story: **lineage, provenance, metadata, schema, name, UUID, and
  version**.

By construction, a Hermes dataset is never "just a file" — it is a file plus the story of how it was
produced and what it contains.

### Convergence requirement

API-sourced data and file-sourced data must converge into the **same internal representation**, so all
downstream stages (normalize, validate, profile, query, export) behave identically regardless of origin.
Parsing produces the source-agnostic intermediate record representation; normalization maps it onto the
canonical Hermes representation.

---

## Part C — Hermes API and Core Components

`import hermes as hr` is the **canonical public API**. There is **no public `Hermes` class** — it does
not belong in the user-facing interface.

The user should interact with Hermes through the `hr` namespace:

```python
import hermes as hr

data = hr.fetch(...)
data = hr.parse(data)
data = hr.normalize(data)
data = hr.validate(data)

dataset = hr.save(data, ...)
```

The internal implementation can use hundreds of classes, but users should primarily interact with a
relatively small, coherent public API. The classes underneath are implementation objects and data
models. This part is authoritative over the older public-API sketch in
[Part E](#part-e--subsystem-engineering-spec).

### 1. Public API

#### Acquisition

```python
hr.fetch()
hr.fetch_raw()
hr.sync()
```

#### Parsing

```python
hr.parse()
```

#### Transformation

```python
hr.normalize()
hr.transform()
```

#### Inspection / Profiling

```python
hr.inspect()
hr.profile()
```

#### Validation / Quality

```python
hr.validate()
hr.check_quality()
hr.check_completeness()
hr.check_freshness()
hr.check_integrity()
```

#### Entities

```python
hr.resolve_entity()
hr.resolve_company()
hr.resolve_country()
hr.resolve_security()
hr.resolve_organization()
hr.resolve_person()
```

#### Metadata

```python
hr.get_metadata()
```

#### Datasets

```python
hr.list_datasets()            # Result of stored dataset names
DatasetCatalog().load()       # real catalog: DatasetDescriptor index (list/get/search/register)
hr.dataset()                  # roadmap (E11 catalog API)
hr.search_datasets()          # roadmap (E11 catalog API)
```

#### Storage

```python
hr.save()
hr.load()
hr.materialize()
hr.delete()
```

#### Query

```python
hr.query()
```

#### Provenance

```python
hr.get_provenance()
hr.trace_provenance()
```

#### Lineage

```python
hr.get_lineage()
hr.trace_lineage()
```

#### Versioning

```python
hr.version()
hr.snapshot()
hr.diff()
hr.restore()
```

#### Schemas

```python
hr.get_schema()
hr.register_schema()
hr.compare_schema()
hr.migrate()
```

#### Connectors

```python
hr.connectors()
```

#### Credentials

```python
hr.credentials()
```

The important distinction is:

```python
import hermes as hr
```

is the **public interface**. The classes underneath are implementation objects and data models.

### 2. Core Classes

These are the fundamental objects Hermes needs.

```text
Dataset
DatasetRef
Result

Metadata
Provenance
Lineage
Version
Snapshot

Schema
SchemaField
SchemaRegistry

Entity
EntityIdentifier
EntityAlias
EntityRelationship
EntityRegistry
MatchResult
MatchEvidence
```

There is **no public `Hermes` class**.

### 3. Dataset

This is one of the most important abstractions in Hermes.

```python
class Dataset:
    id
    name
    version
    schema
    metadata
    provenance
    lineage
    quality
    storage
    source
```

Methods:

```python
dataset.head()
dataset.tail()
dataset.count()

dataset.schema()
dataset.metadata()

dataset.inspect()
dataset.profile()

dataset.validate()

dataset.save()
dataset.load()

dataset.query()

dataset.snapshot()
dataset.diff()

dataset.get_provenance()
dataset.get_lineage()
```

A `Dataset` does **not** necessarily mean that the entire dataset is sitting in RAM. It can reference:

```text
CSV
Parquet
Arrow
DuckDB
PostgreSQL
filesystem
remote dataset
Hermes Cloud dataset
```

For example:

```python
import hermes as hr

dataset = hr.load("companies.parquet")

dataset.inspect()
dataset.profile()
dataset.query(...)
```

### 4. DatasetRef

A lightweight reference to a dataset.

```python
class DatasetRef:
    id
    name
    version
    location
    storage
```

This allows Hermes to pass datasets around without necessarily materializing them.

For example:

```python
ref = DatasetRef(
    name="companies",
    location="data/companies.parquet",
)
```

### 5. Result

Hermes functions should return predictable result objects rather than completely unrelated return
types.

```python
class Result:
    data
    metadata
    warnings
    errors
    statistics
```

Specialized results:

```text
FetchResult
ParseResult
NormalizeResult
ValidationResult
InspectionResult
ProfileResult
MatchResult
QueryResult
```

For example:

```python
result = hr.parse(raw)

result.data
result.errors
result.warnings
result.statistics
```

### 6. Acquisition

```text
hermes/acquisition/
```

#### Client

```python
class Client:
    get()
    post()
    put()
    delete()
    request()
    stream()
```

#### Cache

```python
class Cache:
    get()
    set()
    exists()
    delete()
    clear()
```

#### RetryPolicy

```python
class RetryPolicy:
    should_retry()
    get_delay()
```

#### RateLimiter

```python
class RateLimiter:
    acquire()
    wait()
```

#### Paginator

```python
class Paginator:
    paginate()
```

#### SyncEngine

```python
class SyncEngine:
    sync()
    incremental_sync()
    full_sync()
    detect_changes()
```

Public functions:

```python
hr.fetch()
hr.fetch_raw()
hr.sync()
```

### 7. Connectors

Every connector should implement a common interface.

```python
class Connector:
    name
    version
    capabilities
    credentials

    connect()
    fetch()
    fetch_raw()
    metadata()
    health()
```

Example:

```text
hermes/connectors/
├── sec/
├── fred/
├── imf/
├── world_bank/
├── gdelt/
├── opensanctions/
├── binance/
├── finnhub/
└── yfinance/
```

A connector can contain source-specific functionality.

For example:

```python
class SECConnector(Connector):
    fetch_companies()
    fetch_filings()
    fetch_facts()
```

The important rule:

**Generic functionality belongs in Hermes core. Source-specific behavior belongs in connectors.**

### 8. Connector Registry

```python
class ConnectorRegistry:
    register()
    unregister()
    get()
    list()
    discover()
```

Internally:

```python
registry.get("sec")
registry.get("fred")
```

Publicly:

```python
hr.connectors()
```

### 9. Parsing

```text
hermes/parsing/
```

#### Parser

```python
class Parser:
    parse()
    parse_stream()
    can_parse()
```

#### ParsingEngine

```python
class ParsingEngine:
    parse()
    parse_stream()
    register_parser()
    get_parser()
```

#### ParsedRecord

```python
class ParsedRecord:
    data
    raw
    source
    location
    metadata
    warnings
    errors
```

#### ParseResult

```python
class ParseResult:
    records
    warnings
    errors
    statistics
```

Built-in parsers:

```text
CSVParser
JSONParser
JSONLParser
XMLParser
ParquetParser
ArrowParser
```

Public:

```python
hr.parse(...)
```

Internal helpers can include:

```python
parse_csv()
parse_json()
parse_jsonl()
parse_xml()
parse_parquet()
parse_arrow()
```

These don't necessarily need to be exposed at the top-level API.

### 10. Normalization

```text
hermes/normalization/
```

#### NormalizationEngine

```python
class NormalizationEngine:
    normalize()
    normalize_stream()
    register_rule()
```

#### NormalizationRule

```python
class NormalizationRule:
    apply()
    validate()
```

Rules:

```text
MapField
RenameField
DropField
CastType
ConvertUnit
NormalizeString
NormalizeDate
NormalizeCountry
NormalizeCurrency
NormalizeIdentifier
NormalizeName
MapConcept
ParsePeriod
```

Example:

```python
rules = [
    RenameField("Country", "country"),
    NormalizeCountry("country"),
    CastType("value", float),
    ConvertUnit("value", "USD"),
]
```

Public:

```python
hr.normalize(data)
```

The engine executes the rules.

### 11. Validation

```text
hermes/validation/
```

#### ValidationEngine

```python
class ValidationEngine:
    validate()
    validate_stream()
    register_check()
```

#### ValidationResult

```python
class ValidationResult:
    valid
    errors
    warnings
    statistics
```

Checks:

```text
NotNull
Unique
UniqueCombination
TypeCheck
RangeCheck
EnumCheck
RegexCheck
ForeignKeyCheck
DateRangeCheck
SchemaCheck
FreshnessCheck
CompletenessCheck
ReferentialIntegrityCheck
```

Example:

```python
checks = [
    NotNull("company_id"),
    Unique("company_id"),
    EnumCheck(
        "currency",
        ["USD", "EUR", "GBP"],
    ),
]
```

Public:

```python
hr.validate(data)
```

### 12. Inspection

Inspection answers: **what is this dataset?**

```text
hermes/inspection/
```

#### Inspector

```python
class Inspector:
    inspect()
    sample()
    schema()
    shape()
    columns()
```

#### InspectionResult

```python
class InspectionResult:
    rows
    columns
    fields
    sample
    dtypes
    nulls
    duplicates
    nested_fields
```

Functions:

```python
inspect()
sample()
infer_schema()
detect_columns()
detect_nested()
detect_duplicates()
detect_candidate_keys()
```

Public:

```python
hr.inspect(data)
```

### 13. Profiling

Profiling answers: **what does this dataset statistically look like?**

```text
hermes/profiling/
```

#### Profiler

```python
class Profiler:
    profile()
    profile_column()
    profile_dataset()
```

Profiles:

```text
NumericProfile
StringProfile
CategoricalProfile
TemporalProfile
DatasetProfile
```

Functions:

```python
describe_numeric()
describe_categorical()
describe_temporal()

calculate_quantiles()
calculate_frequency()
calculate_cardinality()
calculate_null_rate()
calculate_uniqueness()
```

Public:

```python
hr.profile(data)
```

### 14. Metadata

```text
hermes/metadata/
```

#### Metadata

```python
class Metadata:
    dataset_id
    name
    description
    source
    created_at
    updated_at
    schema
    format
    row_count
    column_count
    connector
```

#### MetadataExtractor

```python
class MetadataExtractor:
    extract()
    extract_schema()
    extract_statistics()
    extract_source()
```

#### MetadataRegistry

```python
class MetadataRegistry:
    register()
    get()
    update()
    delete()
    search()
    list()
```

Public:

```python
hr.get_metadata(dataset)
```

### 15. Entity Resolution

This should be one of Hermes' major systems.

```text
hermes/entities/
```

#### Entity

```python
class Entity:
    id
    entity_type
    canonical_name
    country_id
    identifiers
    aliases
    attributes
```

#### EntityIdentifier

```python
class EntityIdentifier:
    namespace
    value
    source
    valid_from
    valid_to
```

Examples:

```text
SEC CIK
LEI
ISIN
CUSIP
national registration number
OpenSanctions ID
source-specific ID
```

#### EntityAlias

```python
class EntityAlias:
    value
    normalized_value
    alias_type
    source
```

#### EntityRelationship

```python
class EntityRelationship:
    source_entity
    relationship
    target_entity
    valid_from
    valid_to
    source
```

Examples:

```text
Apple Inc. -> issued -> AAPL
Company X -> located_in -> Pakistan
Person X -> director_of -> Company X
Company X -> subsidiary_of -> Company Y
Company X -> sanctioned_by -> OFAC
```

### 16. Entity Registry

```python
class EntityRegistry:
    add()
    get()
    update()
    delete()

    find_by_identifier()
    find_by_alias()
    find_by_name()

    link()
    unlink()

    relationships()
```

### 17. Entity Resolver

```python
class EntityResolver:
    resolve()
    generate_candidates()
    compare()
    score()
    explain()
```

Matching:

```python
class MatchResult:
    entity_id
    score
    decision
    evidence
```

```python
class MatchEvidence:
    field
    method
    result
    weight
```

Useful internal functions:

```python
normalize_name()
normalize_identifier()

generate_candidates()

calculate_name_similarity()
calculate_token_similarity()
calculate_attribute_similarity()

score_match()
explain_match()
```

Public:

```python
hr.resolve_entity(...)
hr.resolve_company(...)
hr.resolve_country(...)
hr.resolve_security(...)
hr.resolve_organization(...)
hr.resolve_person(...)
```

### 18. Schema System

```text
hermes/schemas/
```

#### Schema

```python
class Schema:
    name
    version
    fields
    namespace
```

#### SchemaField

```python
class SchemaField:
    name
    type
    nullable
    required
    description
    semantic_type
```

#### SchemaRegistry

```python
class SchemaRegistry:
    register()
    get()
    list()
    compare()
    migrate()
```

Functions:

```python
infer_schema()
validate_schema()
compare_schema()
migrate_schema()
```

Canonical schemas can include:

```text
Entity
Company
Person
Organization
Country

FinancialStatement
Security
MarketData

EconomicIndicator

GeopoliticalEvent
Conflict
Sanction
MilitaryAsset

Document
```

### 19. Storage

```text
hermes/storage/
```

#### Storage

```python
class Storage:
    save()
    load()
    delete()
    exists()
    list()
    metadata()
```

Implementations:

```text
FilesystemStorage
ParquetStorage
DuckDBStorage
```

Future:

```text
PostgresStorage
S3Storage
HermesCloudStorage
```

Public:

```python
hr.save()
hr.load()
hr.delete()
hr.materialize()
```

### 20. Query Engine

```text
hermes/query/
```

#### QueryEngine

```python
class QueryEngine:
    query()
    filter()
    select()
    sort()
    group()
    aggregate()
```

Objects:

```text
Query
Filter
Expression
Condition
Sort
Aggregation
```

Example:

```python
result = hr.query(
    "companies",
    country="PK",
    revenue__gt=1_000_000_000,
)
```

Or:

```python
result = dataset.query().filter(country="PK").select("name", "revenue").execute()
```

### 21. Provenance

```text
hermes/provenance/
```

#### Provenance

```python
class Provenance:
    source
    source_url
    connector
    retrieved_at
    raw_hash
    transformation
```

#### ProvenanceRecord

```python
class ProvenanceRecord:
    dataset_id
    record_id
    source
    source_record
    transformations
    timestamp
```

#### ProvenanceTracker

```python
class ProvenanceTracker:
    record()
    get()
    trace()
```

Functions:

```python
get_provenance()
trace_provenance()
hash_record()
hash_dataset()
```

A Hermes record should be traceable like:

```text
final record
    ↓
entity resolution
    ↓
normalization
    ↓
parsing
    ↓
source record
    ↓
source
```

### 22. Lineage

```text
hermes/lineage/
```

#### Lineage

```python
class Lineage:
    dataset_id
    parents
    transformations
    children
```

#### LineageGraph

```python
class LineageGraph:
    add()
    remove()

    parents()
    children()

    ancestors()
    descendants()

    trace()
```

Public:

```python
hr.get_lineage()
hr.trace_lineage()
```

### 23. Versioning

```text
hermes/versioning/
```

#### Version

```python
class Version:
    dataset_id
    version
    created_at
    hash
    changes
```

#### Snapshot

```python
class Snapshot:
    dataset_id
    version
    created_at
    hash
    location
```

#### VersionManager

```python
class VersionManager:
    create()
    get()
    list()
    compare()
    restore()
```

Public:

```python
hr.version()
hr.snapshot()
hr.diff()
hr.restore()
```

### 24. Dataset Registry / Catalog

```text
hermes/datasets/
```

#### DatasetRegistry

```python
class DatasetRegistry:
    register()
    unregister()
    get()
    list()
    search()
```

#### DatasetCatalog

```python
class DatasetCatalog:
    search()
    discover()
    describe()
    dependencies()
```

Public:

```python
hr.dataset()
hr.datasets()
hr.search_datasets()
```

### 25. Export

```text
hermes/export/
```

Exporters:

```text
CSVExporter
JSONExporter
ParquetExporter
ArrowExporter
```

Functions:

```python
export_csv()
export_json()
export_parquet()
export_arrow()
```

Potential public API:

```python
hr.export(data, format="parquet")
```

rather than exposing every exporter.

### 26. Credential System

Don't do:

```python
hr = Hermes(
    fred_api="...",
    sec_email="...",
    ...
)
```

Instead:

```python
class Credential:
    provider
    value
    source
```

```python
class CredentialStore:
    get()
    set()
    delete()
    exists()
```

```python
class CredentialResolver:
    resolve()
    required()
    validate()
```

Usage:

```python
hr.credentials.set("fred", "...")
```

or environment/configuration. Connectors declare what credentials they need.

### 27. Error System

```python
HermesError
```

with specialized errors:

```text
HermesError
├── ConfigurationError
├── ConnectorError
├── AuthenticationError
├── RateLimitError
├── AcquisitionError
├── ParseError
├── NormalizationError
├── ValidationError
├── SchemaError
├── StorageError
├── QueryError
├── EntityResolutionError
├── DatasetError
└── VersionError
```

### 28. CLI

Implemented (`hermes --storage <root>` selects the store):

```bash
hermes fetch <connector-or-file> [dataset]
hermes inspect <file-or-name>
hermes profile <file-or-name> [--json]
hermes entity resolve <query> [--type country|company|security|...]
hermes dataset list | info <name> | delete <name>
```

Planned:

```bash
hermes parse data.csv
hermes normalize data.csv
hermes validate data.csv

hermes save data.csv
hermes load companies

hermes schema list
hermes schema show company

hermes lineage companies
hermes provenance companies

hermes version companies
hermes diff companies:v1 companies:v2
```

### 29. Actual Hermes Package Structure

Putting everything together:

*The tree below is illustrative. Reality since Phases 1–10: the public surface lives in `hermes/api/`; metadata/provenance/lineage/versioning/inspection models live in `hermes/core/` (not separate top-level packages); `entities/` has no `companies.py`/`countries.py` (seeds come from `hermes/resources/countries.py` + `connectors/lib/datasets/cik.parquet`); storage is `hermes/storage/filesystem.py` with metadata/format handling inline (no `parquet.py`/`duckdb.py`); CLI is `hermes/cli`; credentials live in `hermes/credentials`.*

```text
hermes/
├── __init__.py
│
├── acquisition/
│   ├── client.py
│   ├── cache.py
│   ├── pagination.py
│   ├── retry.py
│   ├── rate_limit.py
│   └── sync.py
│
├── connectors/
│   ├── base.py
│   ├── registry.py
│   ├── sec/
│   ├── fred/
│   ├── imf/
│   ├── world_bank/
│   ├── gdelt/
│   ├── opensanctions/
│   ├── binance/
│   ├── finnhub/
│   └── yfinance/
│
├── parsing/
│   ├── engine.py
│   ├── parser.py
│   ├── records.py
│   └── errors.py
│
├── normalization/
│   ├── engine.py
│   ├── rules.py
│   ├── mapping.py
│   └── errors.py
│
├── validation/
│   ├── engine.py
│   ├── checks.py
│   ├── contracts.py
│   ├── reports.py
│   └── errors.py
│
├── inspection/
│   ├── inspector.py
│   └── models.py
│
├── profiling/
│   ├── profiler.py
│   └── models.py
│
├── metadata/
│   ├── extractor.py
│   ├── models.py
│   └── registry.py
│
├── entities/
│   ├── models.py
│   ├── registry.py
│   ├── resolver.py
│   ├── aliases.py
│   ├── countries.py
│   └── companies.py
│
├── schemas/
│   ├── base.py
│   ├── registry.py
│   ├── entity.py
│   ├── financial.py
│   ├── market.py
│   ├── economic.py
│   ├── geopolitical.py
│   └── security.py
│
├── datasets/
│   ├── registry.py
│   ├── catalog.py
│   └── models.py
│
├── storage/
│   ├── base.py
│   ├── filesystem.py
│   ├── parquet.py
│   └── duckdb.py
│
├── query/
│   ├── engine.py
│   ├── filters.py
│   └── expressions.py
│
├── provenance/
│   ├── models.py
│   └── tracker.py
│
├── lineage/
│   ├── models.py
│   └── graph.py
│
├── versioning/
│   ├── models.py
│   └── manager.py
│
├── export/
│   ├── csv.py
│   ├── json.py
│   ├── parquet.py
│   └── arrow.py
│
├── credentials/
│   ├── models.py
│   ├── store.py
│   └── resolver.py
│
└── errors.py
```

### 30. The Core Public API

The whole thing ultimately exposes:

```python
import hermes as hr
```

#### Data acquisition

```python
hr.fetch()
hr.fetch_raw()
hr.sync()
```

#### Data understanding

```python
hr.inspect()
hr.profile()
hr.get_metadata()
```

#### Data processing

```python
hr.parse()
hr.normalize()
hr.transform()
```

#### Data verification

```python
hr.validate()
hr.check_quality()
hr.check_completeness()
hr.check_freshness()
hr.check_integrity()
```

#### Entity intelligence

```python
hr.resolve_entity()
hr.resolve_company()
hr.resolve_country()
hr.resolve_security()
hr.resolve_organization()
hr.resolve_person()
```

#### Dataset management

```python
hr.dataset()
hr.datasets()
hr.search_datasets()

hr.save()
hr.load()
hr.materialize()
hr.delete()
```

#### Query

```python
hr.query()
```

#### Data history

```python
hr.get_provenance()
hr.get_lineage()

hr.version()
hr.snapshot()
hr.diff()
hr.restore()
```

#### Schemas

```python
hr.get_schema()
hr.register_schema()
hr.compare_schema()
hr.migrate()
```

### 31. What Hermes should feel like

A developer should be able to do this:

```python
import hermes as hr

raw = hr.fetch_raw("sec")

parsed = hr.parse(raw)

normalized = hr.normalize(parsed)

resolved = hr.resolve_entity(normalized)

validated = hr.validate(resolved)

dataset = hr.save(
    validated,
    name="companies",
)
```

Then:

```python
dataset.inspect()
dataset.profile()
```

And:

```python
dataset.query(country="PK")
```

And:

```python
hr.get_provenance(dataset)
hr.get_lineage(dataset)
```

And:

```python
hr.diff(
    "companies:v1",
    "companies:v2",
)
```

The important design is now:

```text
                 import hermes as hr
                          │
       ┌──────────────────┼──────────────────┐
       ↓                  ↓                  ↓
   Acquisition       Processing          Intelligence
       │                  │                  │
     fetch         parse/normalize      entities
       │            validate             schemas
       ↓                  │                  │
                    Dataset ◄───────────────┘
                       │
            ┌──────────┼──────────┐
            ↓          ↓          ↓
         Storage    Provenance   Lineage
            │          │          │
            └──────────┼──────────┘
                       ↓
                     Query
```

Hermes does **not** expose every internal class through `hermes/__init__.py`. The public API stays
clean — `import hermes as hr` — while the internal implementation can evolve independently.

## Part D — Architecture

### Package layout (current)

```text
hermes/
├── __init__.py            # Public facade
├── acquisition/           # cache · client · retry · rate_limit · pagination · sync
├── api/                   # acquire · data · datasets · entities · schemas · storage
├── cli/                   # hermes commands
├── connectors/            # binance · finnhub · fred · gdelt · imf · opensanctions ·
│                          # public_data · sec · world_bank · yfinance
├── constants.py
├── core/                  # dataset · errors · lineage · metadata · provenance · result · versioning · config
├── datasets/              # catalog · models · registry
├── entities/              # aliases · companies · countries · models · registry · resolver
├── export/                # csv · json · parquet · arrow
├── features/              # (de-scoped) financial · country_risk · decorator · registry
├── metadata/              # extractor · models · registry
├── normalization/         # engine · mapping · rules · errors
├── parsing/               # engine · records · csv_parser · json_parser · parquet_parser · xml_parser · errors
├── query/                 # engine · filters · expressions
├── schemas/               # base · registry · entity · document · economic · financial · market · geopolitical · security
├── storage/               # base · filesystem · parquet · duckdb
└── validation/            # engine · checks · contracts · reports · errors

data/datasets/             # bundled static datasets
tests/                     # unit · connectors · features · integration
```

### Responsibilities by subsystem

| Subsystem | Owns | Not owned here |
|---|---|---|
| `__init__.py` | Public `hr.*` facade | feature logic |
| `api/` | Thin translation of user ops → internal ops | business logic |
| `acquisition/` | HTTP client, caching, retry, rate limiting, pagination, sync | per-source fetches |
| `connectors/` | Per-source acquisition + parse/normalize/map/schema | generic infrastructure |
| `core/` | Dataset, errors, metadata, provenance, lineage, versioning | domain logic |
| `schemas/` | Canonical schema registry, versions, migration | acquisition |
| `parsing/` | Format → structured records | semantic normalization |
| `normalization/` | Source → canonical normalization | acquisition logic |
| `validation/` | Checks, contracts, reports; errors vs warnings | source knowledge |
| `metadata/` | Descriptive metadata extraction | data modification |
| `entities/` | Entity registry, aliases, resolution | data acquisition |
| `datasets/` | Dataset catalog & registry | persistence engine |
| `storage/` | Where datasets persist | query execution |
| `query/` | Filtering/projection/aggregation/joins/SQL | storage layout |
| `export/` | To external formats/tools | caching |
| `features/` | (de-scoped) derived analytics | connector I/O |

### Canonical schemas

A canonical schema is the contract between sources and the rest of Hermes:

```text
Source A ─→ Mapping ─→ Canonical Hermes Schema ←─ Mapping ←─ Source B
```

The v1 canonical schemas are: **Entity · Economic observation · Financial observation · Market
observation · Geopolitical event · Security event · Document**. Each defines field names, types,
required/optional fields, primary keys, entity references, units, temporal semantics, allowed values,
constraints, and a **schema version**. Canonical schemas are domain-specific — never one giant
universal schema.

### Connector package convention

Each connector ships source-specific modules only, with generic behavior living in the shared
subsystems:

```text
source/
├── __init__.py
├── connector.py     # source integration: endpoints, params, acquisition orchestration
├── parser.py        # raw response → structured records
├── normalizer.py    # source → canonical mapping
└── mappings.py      # endpoint tables, field/identifier/unit mappings
```

A connector should (1) acquire, (2) preserve raw data, (3) parse, (4) map fields to Hermes concepts,
(5) normalize values, (6) declare the canonical schema, (7) validate output, (8) provide metadata and
provenance. A connector must NOT implement generic retry/caching/validation, business logic, or feature
engineering.

### Architectural boundaries

```text
Connector      knows source API/format/concepts            · no generic retry/cache/storage
Acquisition    knows how to reliably retrieve data         · does not know what GDP/revenue means
Parser         knows how to interpret the source format    · does not define canonical meaning
Normalizer     knows how to make data consistent           · generic rules global, source mapping in connector
Schema         defines what canonical data looks like
Validation     determines whether data satisfies requirements
Metadata       describes what the dataset contains
Provenance     describes where the dataset came from
Lineage        describes what happened to the dataset
Storage        where the dataset is persisted
Query          how stored datasets are accessed
Export         how data transfers to external tools
```

**Dependency rule:** Core must not depend on any domain package; domain packages may depend on Core.
Generic behavior → Hermes subsystem; source-specific behavior → connector; canonical meaning → schema;
derived analytical behavior → features.

### Data flow

```text
External Source
      ↓
Connector
      ↓
Acquisition → Raw response → Parser → Structured records → Source mapping → Normalization
      ↓
Canonical Hermes Schema → Validation → Metadata → Provenance → Lineage
      ↓
Hermes Dataset
      ↓
┌──────────┬──────────┬──────────┐
Storage    Query      Export     Features (de-scoped)
```

---

## Part E — Subsystem Engineering Spec

**How to read this:** every unchecked box is an engineering task. Assignments follow the team/ownership
map in [Part F](#part-f--engineering-team). DoD = Definition of Done.

### E0. Project direction

**Objective:** evolve Hermes into a reusable data platform that can *acquire, preserve raw data, parse,
normalize to canonical schemas, validate, profile, attach metadata, track provenance + lineage, resolve
entities, register/version datasets & schemas, store/query, export, and synchronize incremental
updates* — and serve finance/defense datasets through an entity-centric provider API.

Core principle:

```text
External Source → Connector → Raw Data → Parse → Normalize → Validate
→ Metadata + Provenance + Lineage → Hermes Dataset → Storage / Query / Export
```

### E1. Core Dataset System

*Status: core implemented — `Dataset`, `Result`, error taxonomy, and the metadata/provenance/lineage/version models exist. Save/export, load, inspect, profile work; `DatasetCatalog` (descriptor index over stored datasets) implemented; query engine pending.*

- [x] Create `Dataset` abstraction
- [x] Define dataset identity
- [x] Define dataset name
- [x] Define dataset ID
- [x] Define dataset schema reference
- [x] Define dataset version
- [x] Define dataset metadata reference
- [x] Define provenance reference
- [x] Define lineage reference
- [x] Create standardized operation/result objects (`Result`, `ValidationResult`, `NormalizationResult`)
- [x] Create standardized error handling (`HermesError` hierarchy)
- [x] Ensure datasets are independent of specific storage engines

Dataset requirements: contains schema info, metadata, provenance, lineage, version; supports
lazy/eager execution where appropriate; integrates with Arrow, Polars, Pandas, DuckDB; operations
`parse normalize validate profile inspect transform resolve query save export metadata schema lineage`
return consistent `Dataset`/result types.

### E2. Acquisition Engine

*Status: partial — `RawCache` (Parquet disk cache with TTL/keys/stats) and `Client` (Rust core HTTP: retries, backoff, error mapping, streaming) implemented and used by all connectors. `fetch`/`fetch_raw`/`read`/`ingest`/`sync` top-level API implemented for registered sources (binance, finnhub, fred, imf, opensanctions, sec, world_bank, yfinance); local files ingest via path. NOT implemented: sync state persistence, pagination helpers.*

- [ ] Define `Source`: configuration, credentials, capabilities, metadata, lifecycle
- [ ] Implement `fetch()`, `ingest()`, `source()`, `connect()`, `read()`, `stream()`
- [ ] API sources, file sources, local sources supported
- [ ] Streaming sources have a defined interface
- [ ] Failures produce structured errors
- [ ] Source information is recorded in provenance
- [ ] Common HTTP client with headers/timeouts/response handling
- [ ] Cache: keys, expiration, invalidation (move current cache implementation)
- [ ] Retry: timeouts, temporary server errors, connection failures, rate-limit responses
- [ ] Pagination: pages/offsets/cursors/next-URL/date-range/tokens
- [ ] Rate limiting: tracking, waiting, response handling
- [ ] Synchronization: sync state, last-successful-sync, cursors, timestamps
- [ ] Resumable acquisition; request timeout handling
- [ ] Implement `fetch_raw()`, `sync()`; preserve existing `_fetch()` acquisition abstraction

### E3. Parsing Engine

*Status: IMPLEMENTED. `ParserEngine.parse()`/`detect_format()` real; CSV/JSON/JSONL/Parquet/XML parsers return `pl.DataFrame`; powers `hr.parse()` and `Dataset.load()`. Not ended: Arrow/compressed files, nested-JSON flattening, malformed-record classification (single `ParseError`).*

- [x] Define `Parser` contract: input contract, output contract, registration, selection
- [x] Implement `parse()`, `detect_format()`, `read_raw()`, `decode()`
- [x] Formats: CSV, JSON, JSONL, XML, Parquet
- [ ] Formats: Arrow, compressed files
- [ ] Nested JSON and lists-of-records support
- [ ] Intermediate record representation (`records.py`)
- [ ] Preserve source fields and raw values
- [ ] Handle malformed records; define parser errors and warnings
- [ ] Allow connector-specific parsers; keep source-specific logic inside connectors
- [x] Prevent generic parser from containing SEC/GDELT business logic
- [x] Parser does not perform semantic normalization, entity resolution, or contain domain mappings

### E4. Schema / Data Contract Engine

*Status: implemented — `Schema`/`FieldDef` models + 7 canonical schemas registered (`economic.observation`, `financial.observation`, `market.observation`, `geopolitical.event`, `security.event`, `entity`, `document`). `SchemaRegistry` (register/get/latest semver/compatibility/migrate) + top-level `get_schema`/`register_schema`/`compare_schema`/`migrate` implemented. NOT implemented: infer_schema from data, migration backfill.*

- [x] Define schema model: fields, types, nullable, required, constraints
- [ ] Schema versioning and serialization
- [ ] Implement `schema()`, `register_schema()`, `infer_schema()`, `validate_schema()`,
      `compare_schema()`, `migrate_schema()`, `metadata()`, `set_metadata()`
- [ ] Schema registry, compatibility checking, evolution, version tracking, migration
- [x] Initial canonical schemas registered: entity, economic, financial, market, geopolitical,
      security, document

### E5. Normalization Engine

*Status: IMPLEMENTED. `NormalizationEngine` (normalize/normalize_record/normalize_stream/normalize_report) + 17 rules (Rename, Cast, NormalizeString/Null/Boolean/Date/Country/Currency/Unit, ConvertUnit, NormalizeIdentifier/Name, MapValue, MapConcept, ParsePeriod, StripCharacters, Round). Not ended: automated lineage recording of normalization steps.*

- [x] Define normalization interface; source→canonical mapping
- [x] Type, unit, temporal, geographic, identifier normalization
- [ ] Implement `normalize()`, `map()`, `cast()`, `standardize()`, `convert_units()`, `align_time()`,
      `clean()`
- [x] ISO date/time conventions; consistent timezone handling
- [x] Standard country codes; consistent numeric types; unit conversion framework
- [x] Currency normalization; missing-value conventions; duplicate handling
- [x] Source-specific mappings remain outside generic Core
- [ ] Normalization is deterministic; steps recorded in lineage
- [x] Normalization rules reusable (`rules.py`: date, numeric, string cleanup, null, unit, identifier)

### E6. Quality Engine

*Status: `validate()` + 22 rules implemented; `profile()` (stats, quality info, frequency/date-range/anomaly detection) implemented. Not ended: `ValidationReport` score/model, severity levels, the additional `check_*` wrappers.*

- [x] Define quality-check and validation-rule interfaces
- [ ] Define quality report, score/model, severity levels, warning vs error behavior
- [ ] Implement `validate()`, `check()`, `check_quality()`, `check_completeness()`,
      `check_freshness()`, `check_integrity()`
- [x] Checks: null, type, range, required-field, constraint, schema, primary-key, foreign-key,
      referential-integrity, unit, date, duplicates
- [ ] Create `ValidationReport`; separate errors from warnings
- [ ] Profiling: row count, column count, types, null %, unique, duplicates, min/max, basic stats,
      distributions, temporal coverage, frequency detection, gap detection
- [ ] Implement `profile()`
- [ ] Deduplication: exact, configurable keys, resolution strategy, preserve duplicates when required
- [ ] Anomaly detection: extensible interface, not coupled to ML implementations
- [ ] Quality results recorded in metadata/provenance; machine- and human-readable reports

### E7. Metadata System

*Status: partial — `MetaData`, `ColumnMetadata`, `QualityInfo`, `InspectReport` models + `profile()`/`inspect()`/`get_freqs()`/`date_ranges()`/`anomaly_count()` implemented.*

- [x] Dataset-level and column-level metadata models
- [ ] Type, row/column counts, null stats, unique stats, date range, frequency detection,
      entity coverage, source information, retrieval timestamp, last-observation timestamp,
      expected update frequency, quality information
- [ ] Implement `get_metadata()`, `inspect()`, `profile()`
- [x] Metadata does not modify the dataset

### E8. Provenance

- [ ] Define provenance model
- [ ] Record source, URL/API endpoint, retrieval timestamp, connector, connector version,
      raw-data checksum, parser version, normalizer version, schema version, validation result,
      transformation information
- [ ] Implement `get_provenance()`
- [ ] Provenance immutable once recorded where appropriate

### E9. Lineage

- [ ] Define lineage model
- [ ] Track input/output dataset, operations, transformations, timestamps, versions, parameters
- [ ] Build dataset lineage graph; implement `get_lineage()`; make lineage queryable
- [ ] Start with ordered lineage records; design so a DAG can be added later; do not build a DAG initially

### E10. Entity System *(first-class pillar)*

*Status: implemented — `Entity`/`EntityMatch` models, `Resolver` ABC, `EntityRegistry`, seeds (249 ISO-3 countries via `countries_frame()`, ~8k SEC CIK → company entities via `cik.parquet`), aliases (`add_alias`/`resolve_alias`/`list_aliases`), and `resolve_entity/country/company/security/organization/person` top-level API; variably-typed entities resolve by name/identifier/alias, `resolve_data` maps key columns to entity ids. NOT implemented: ~100k-entity registry, fuzzy matcher tuning.*

- [x] Define `Entity` and `EntityMatch` models; canonical entity representation
- [x] Define `Resolver` interface: `resolve()`, `identify()`, `match()`, `link()`, `entity()`
- [ ] Registry: `register()`, `get()`, `resolve()`, `list_types()`
- [ ] Aliases: `add_alias()`, `resolve_alias()`, `list_aliases()`
- [x] Countries: canonical IDs, ISO-2/ISO-3/name/numeric-code resolution, aliases,
      historical/source-specific identifiers, `resolve_country()`
- [x] Companies: canonical IDs, name, ticker, CIK, LEI, ISIN, source-specific IDs, aliases,
      `resolve_company()`
- [ ] Persons: canonical IDs, name/identifier resolution, aliases (defense/persons scope)
- [ ] Implement `resolve_entity()`
- [ ] Connect entities to canonical schemas
- [ ] **Entity registry populated to ~100k entities: companies, countries, and persons for finance & defense**
- [ ] **Entity-centric provider API:** `hr.resolve_company("AAPL")` → `.financials`, `.market_data`,
      `.fillings`, extensible per-domain datasets

Core provides the resolver interface; domain-specific entity knowledge stays outside Core.
Corporate/financial/defense/healthcare identifiers can be added independently.

### E11. Dataset Catalog

- [ ] Define dataset registry and identifier
- [ ] Fields: description, owner/source, schema, versions, coverage, frequency, quality, freshness,
      provenance
- [ ] Implement `datasets.list()`, `datasets.get()`, `datasets.search()`
- [ ] Register each bundled static dataset with schema, metadata, validation, provenance, version

### E12. Storage

- [ ] Define storage abstraction; pluggable backends
- [ ] Filesystem backend; Parquet backend (partitioning, compression, manifests); DuckDB integration
- [ ] Dataset layout: partition strategy, compression, manifests
- [ ] Persist metadata, schema, version, provenance with data
- [ ] Implement `save()`, `load()`, `delete()`, existence checks
- [ ] Atomic writes; corruption protection; storage tests

### E13. Query Engine

- [ ] Define query interface and execution model; query result abstraction
- [ ] Implement `query()` and `sql()`
- [ ] Filtering, projections, joins, aggregations, ordering, limits, entity/date/range filtering
- [ ] DuckDB execution; Polars/Arrow/Pandas integration
- [ ] Query separated from storage; query tests

### E14. Materialization

- [ ] Define materialization abstraction
- [ ] Materialize to Polars, Pandas, Arrow, DuckDB relation
- [ ] Implement `materialize()`; never mutate canonical data

### E15. Export

*Status: partial — `export()` real (csv/json/parquet) and `Dataset.save()`/`.export()` incl. to_polars/to_arrow/to_pandas. NOT implemented: `to_duckdb()`, metadata-preserving export.*

- [ ] Define exporter interface and configuration; export metadata
- [ ] Implement `export()`, `to_arrow()`, `to_polars()`, `to_pandas()`, `to_duckdb()`
- [x] Formats: Parquet, CSV, JSON, JSONL, Arrow
- [ ] Preserve metadata/schema/provenance where supported

### E16. Dataset Versioning

- [ ] Version model: dataset, schema, pipeline, version identifiers, version metadata
- [ ] Implement `version()`, `snapshot()`, `diff()`
- [ ] Content hashing, schema hashing, transformation versions, deterministic version IDs
- [ ] Immutable snapshots with snapshot metadata/provenance/lineage
- [ ] Detect added/removed/changed rows and schema changes
- [ ] Versioning tests

### E17. Schema Migration

- [ ] Migration model, registry, direction, compatibility rules
- [ ] Detect breaking schema changes; forward migrations
- [ ] Implement `migrate()`; record migration provenance; test reproducibility

### E18. Registry System

- [ ] Component, dataset, schema, connector, parser, validator, transformer, resolver, storage
      registries
- [ ] Implement `register()`, component lookup/discovery/versioning/metadata

### E19. Execution Engine

- [ ] Execution context, pipeline abstraction, state, results, error handling, retry behavior
- [ ] Deterministic stage order; pass `Dataset` between stages
- [ ] Capture lineage, execution metadata, errors automatically
- [ ] Reusable and configurable pipelines

### E20. Inspection / Developer Experience

*Status: implemented — `inspect()` and `profile()` implemented (data API + Dataset methods); CLI (`hermes fetch|inspect|profile|entity|dataset`) wired to the data API. Not ended: `get_metadata`/`get_provenance`/`get_lineage` wrappers, catalog schema/lineage inspection CLI.*

- [ ] Implement `inspect()`: dimensions, schema, metadata, sample records, quality, lineage,
      provenance, version
- [ ] CLI: dataset inspection, schema inspection, profile, validation, lineage, dataset catalog
- [ ] TUI where practical

### E21. Error System

- [ ] Hermes exception hierarchy
- [ ] Acquisition, parsing, schema, normalization, validation, transformation, resolution, storage,
      query, configuration errors
- [ ] Useful error context; preserve original source errors where appropriate

### E22. Extension Architecture

- [ ] Connector interface/config/metadata/lifecycle
- [ ] Plugin interfaces: connector, parser, schema, mapper, normalizer, validator, profiler,
      transformer, resolver, storage backend, exporter
- [ ] Connectors depend on Core, never the reverse

### E23. Python Ecosystem Integration

- [ ] Arrow-native internal interoperability; Arrow/pandas/polars conversions and schema mapping
- [ ] Dataset ↔ Polars, Pandas, DuckDB (SQL execution, parquet querying), NumPy where appropriate

### E24. Public API

*Status: real — `parse`, `normalize`, `transform`, `validate` (incl. `schema=`), `profile`, `inspect`, `resolve_data`, `get_freqs`, `date_ranges`, `anomaly_count`, `Dataset`, `Result`, acquisition (`fetch`/`fetch_raw`/`read`/`ingest`/`sync`), entities (`resolve_entity`/`resolve_country`/`resolve_company`/`resolve_security`/`resolve_organization`/`resolve_person`), schemas (`get_schema`/`register_schema`/`compare_schema`/`migrate`), storage (`save`/`load`/`exists`/`delete`/`list_datasets`/`storage_info`, parquet + IPC), credentials (`set_cred`/`get_cred`/`has_cred`/`list_creds`/`delete_cred`), `configure`/`get_config`. Roadmap-gated (do not build now): `query`/`materialize` (DuckDB query engine), `get_dataset`/`search_datasets` (dataset catalog is `DatasetCatalog` in `hermes.datasets`).*

```python
hr.fetch()            hr.ingest()           hr.read()             hr.sync()
hr.parse()            hr.normalize()        hr.transform()        hr.validate()
hr.profile()          hr.inspect()          hr.get_metadata()     hr.check_quality()
hr.check_completeness() hr.check_freshness() hr.check_integrity()
hr.resolve_entity()   hr.resolve_country()  hr.resolve_company()
hr.datasets.list()    hr.datasets.get()     hr.datasets.search()
hr.save()             hr.load()             hr.query()            hr.materialize()
hr.get_provenance()   hr.get_lineage()      hr.version()          hr.snapshot()      hr.diff()
hr.get_schema()       hr.register_schema()  hr.compare_schema()   hr.migrate()
```

- [ ] Keep the public API thin; route to internal engines; no business logic in wrappers
- [ ] Consistent return types and error behavior
- [ ] Document the public API; add public API tests

`Dataset` methods mirror the `hr.*` ops: `parse normalize validate profile inspect transform resolve
query save export schema metadata lineage`.

### E25. Testing

- [ ] Unit: acquisition, parsing, schema, normalization, validation, profiling, transformation,
      resolution, storage, query, export, versioning, provenance, lineage, registry
- [ ] Integration: API→Parser→Dataset, File→Parser→Dataset, Dataset→Normalize→Validate,
      Dataset→Profile→Quality, Dataset→Store→Load, Dataset→Query→Export, Dataset→Snapshot→Diff,
      full connector pipeline
- [ ] Contract tests: connector, parser, validator, transformer, resolver, storage interfaces
- [ ] Test suite organized as `unit / connectors / features / integration`
- [ ] Regression and failure/recovery tests; schema compatibility tests

### E26. Production Hardening

- [ ] Structured logging; standardized error taxonomy
- [ ] Retry policies, rate-limit handling, request timeouts
- [ ] Memory limits; streaming ingestion; large-file handling
- [ ] Checkpointing; resumable ingestion
- [ ] Atomic dataset writes; corruption detection
- [ ] Deterministic pipelines; reproducibility checks
- [ ] Performance and memory benchmarks; connector reliability tests

### E27. Static Data

- [ ] Move bundled datasets into `data/datasets/`
- [ ] Register each: metadata, schema, validation, provenance, version; catalog access

### E28. v1 Acceptance Criteria

**Acquisition:** reliable connector framework, raw acquisition, cache, retry, pagination, rate limiting,
incremental sync.

**Understanding:** metadata extraction, inspection, profiling.

**Transformation:** parsing, canonical normalization, explicit transformations.

**Trust:** schema validation, quality validation, completeness, freshness, integrity.

**Identity:** country resolution, company resolution, person resolution, general entity resolution,
canonical entity registry (~100k entities).

**Data management:** catalog, registry, storage, querying, materialization, export.

**Reproducibility:** metadata, provenance, lineage, dataset versioning, snapshots, diff, schema
versioning, migration.

**Developer experience:** stable `hr.*` API, connector contract, documented canonical schemas, reference
connector, complete test suite, architecture documentation, connector development documentation.

**Core success tests (both must be CI-green):**

```text
CSV / JSON / API / XML
        ↓
      Hermes
        ↓
Parse → Normalize → Validate
        ↓
Metadata + Provenance + Lineage
        ↓
Canonical Dataset
        ↓
Store → Query → Version → Export
```

```python
import hermes as hr

apple = hr.resolve_company("AAPL")
apple.financials  # CI-verified provider demo
apple.market_data
apple.fillings
```

**The first real milestone is ONE complete vertical slice** (a single source: raw → parse → normalize →
canonical schema → validate → metadata → provenance → stored Dataset), then the rest of Hermes becomes
repeating and generalizing the architecture rather than inventing it per source.

> **Decision on appetite:** "implement everything" is not the milestone. The engine milestone is the
> vertical slice above; the provider milestone is the `resolve_company` demo above.

---

## Part F — Engineering & Team

### Team roles

| Person | Role | Owns |
|---|---|---|
| **Haider** | Founder — architect & core engineer | `core/`, `api/` (design), `schemas/`, `datasets/`, `storage/`+`query/` (design), canonical schemas, connector contract, entity architecture, final review, integration |
| **Abdulrehman** | Core engineer | `connectors/` (rebase), `parsing/`, `export/`, `storage/`+`query/` (implement), source mappings |
| **Abdullah** | Security & core engineer | `acquisition/`, security hardening, storage/query integrity; security review gate on every subsystem |
| **Tasbiha** | Frontend & core engineer | `docs-site/`, public docs, API reference, `inspect()`/CLI display, export helpers |
| **Faik** | Frontend & core engineer | CLI, examples, parser/unit tests, docs-site; grows into core alongside |
| **Ifra** | Core engineer — data quality | `normalization/`, `validation/`, `metadata/`, `entities/` (implementation); schema inference + migration |

### Repository ownership

```text
hermes/
├── api/             → Haider + Abdulrehman
├── acquisition/     → Abdullah
├── connectors/      → Abdulrehman (security review: Abdullah)
├── core/            → Haider
├── schemas/         → Haider (Ifra: inference/migration)
├── parsing/         → Abdulrehman (Faik co-implements CSV/JSON)
├── normalization/   → Ifra
├── validation/      → Ifra
├── metadata/        → Ifra
├── entities/        → Ifra (Haider: design/review)
├── datasets/        → Haider (Tasbiha/Faik: catalog UI + docs)
├── storage/         → Haider + Abdulrehman (Abdullah: integrity)
├── query/           → Haider + Abdulrehman
├── export/          → Abdulrehman + Tasbiha
├── cli/             → Faik (Haider: design)
└── features/        → Shared (de-scoped; keep out of v1-core)
```

Ownership means one person is responsible for understanding, maintaining, testing, and improving a
subsystem — not that others cannot touch it.

### Task rules

Every engineering task must have: **Task ID · Title · Owner · Goal · Background · Input · Expected
output · Files/subsystem · Requirements · Edge cases · Tests · Definition of done.**

Assign `META-001 Implement column metadata extraction` — never "Build metadata."

### Difficulty levels

- **Beginner:** small functions, tests, documentation, simple metadata/validation, small utilities
- **Easy:** small modules, simple connector components, basic parsing, basic mappings
- **Medium:** complete connectors, complex validation, storage, query
- **Hard:** SEC/GDELT normalization, logical entity resolution, schema migrations, lineage, versioning,
  performance
- **Architecture:** only after the engineer understands the subsystem

### Git workflow

Never work directly on `main`. `Issue → Branch → Implementation → Tests → Pull Request → Review →
Merge`. Branch examples: `feature/meta-column-profile`, `feature/worldbank-normalizer`,
`fix/validation-null-check`, `test/sec-normalizer`, `docs/connector-guide`.

### Pull requests

Every PR: *what changed, why, files affected, tests added, tests run, known limitations.* Before
opening: code works, tests added, existing tests pass, no unrelated changes, type hints where
appropriate, docs updated if API changed, no secrets committed.

### Review rules

Author owns correctness. Reviewer checks: correctness, tests, architecture, maintainability, naming,
error handling, API compatibility, performance. The lead reviews: architecture changes, public API
changes, canonical schemas, cross-subsystem changes, entity resolution, storage architecture, major
normalization decisions.

### Coding rules

Prefer: small functions, clear names, type hints, explicit behavior, tests, documentation,
deterministic transformations. Avoid: huge functions, hidden global state, magic behavior, duplicated
infrastructure, source-specific logic in core, untested transformations, unnecessary abstractions.

### The #1 architectural rule

Do not solve the same infrastructure problem separately inside every connector.

```text
Bad:   World Bank → own retry · FRED → own retry · IMF → own retry · SEC → own retry
Good:  Hermes Acquisition {retry, cache, pagination, rate-limit} ← World Bank/FRED/IMF/SEC/...
```

The connector provides source-specific behavior; Hermes provides reusable infrastructure.

### Learning while building

`Python → Git → pytest → Polars → Metadata → Profiling → Validation → Simple parser → Simple connector
→ Normalization → Complete connector`. Every step produces a real PR.

### Communication rules

When blocked, state: *what I am trying to do / what I expected / what actually happened / what I tried /
relevant error / relevant files.*

### Definition of Done (component)

Design understood · implementation exists · interface defined · tests exist · edge cases handled ·
errors handled · documentation exists · metadata/provenance implications considered · code reviewed ·
CI passes.

---

## Part G — Roadmap & Strategy

### v1 scope

v1 = the checkboxes in [Part E](#part-e--subsystem-engineering-spec). Strategy: **core-first** —
build the general data engine so anyone can process their own data (CSV/JSON/XML/Parquet) and so the
finance/defense datasets and data-provider can be built on real infrastructure.

### Quick wins (~half a day)

1. **Truth pass** — README shows "Implemented / Planned"; remove/convert broken root `main.py`
   (`benchmarks/profile_run.py`).  *README largely done.*
2. **License — DONE (2026-09): Elastic License 2.0** (source-available) in `LICENSE.md` +
   `pyproject.toml`; README/docs-site repositioned; commercial path = Hermes Enterprise.
3. **CI gates PRs** — `tests.yml` on `pull_request`, caching, rising coverage threshold; rename
   workflows (`tests` = CI, `publish` = release).
4. **Split-stub demo locked** — local-file core loop as a CI-smoke-tested vertical slice (Phases 1–4
   compressed).

### Phases

**Phase 1 — Core Foundation** *[Blocking] · Haider* (Checklist E1/E7/E21)
`Dataset` lifecycle with conversions, metadata/provenance/lineage/version models, error system,
component ABCs (Parser, Normalizer, Validator, Resolver, StorageBackend).

**Phase 2 — Data In** *[Abdullah day one] · Abdullah + Abdulrehman + Faik* (E2/E3)
Real acquisition (Client/RetryPolicy/RateLimiter/Paginator/SyncState + RawCache), parsing engine
(detect_format + csv/json/parquet/xml parsers → `pl.DataFrame`). Done: `hr.read("file.csv")` returns a
`Dataset`.

**Phase 3 — Data Contract** *[Blocking after Phase 2] · Haider + Ifra* (E4/E5)
Schema registry + 7 canonical schemas + `infer_schema`, normalization engine + reusable rules.
Done: `hr.normalize(df, schema="economic.v1")` → canonical `Dataset`.

**Phase 4 — Data Quality** *· Ifra* (E6/E7)
Validation contracts/checks/reports; profiling + metadata extraction wired into `Dataset.profile()`.

**Phase 5 — Identity & Entity Resolution** *· Ifra, Haider design* (E10)
`Resolver` interface + registry + aliases; countries (ISO2/3/name/numeric) and companies
(ticker/CIK/ISIN) resolvers; `hr.resolve_country("PK")`, `hr.resolve_company("AAPL")` real.

**Phase 6 — Storage / Query / Export / Materialization** *· Haider + Abdulrehman, integrity Abdullah*
(E11/E12/E13/E14/E15)
Filesystem+parquet storage with atomic writes + sidecars; DuckDB backend; exporters; query engine;
dataset catalog.

**Phase 7 — Dataset Lifecycle** *· Haider* (E8/E9/E16/E17/E27)
Automatic provenance + lineage capture; versioning/snapshots/diff; schema migration; bundled static
datasets registered.

**Phase 8 — Public API, CLI, DX** *· Haider + Faik + Tasbiha* (E20/E24)
Thin `hr.*` wrappers with consistent types; CLI commands (`inspect`, `profile`, `validate`, `schema`,
`datasets list`, `lineage`, `sync`); pretty inspect; examples; notebook snippets.

**Phase 9 — Connectors on the Engine** *· Abdulrehman lead, Haider arch, Abdullah security* (E9/S)
`BaseConnector` + registry; World Bank as the reference vertical slice on the `economic` schema; rollout
FRED → IMF → YFinance → Finnhub → Binance → SEC → GDELT → OpenSanctions; STRIDE review per connector.

**Phase 10 — Data Provider (Entity-first serving layer)** *· Ifra + Haider* (E10)
Entity registry scaled to ~100k companies/countries/persons (finance & defense); `resolve_entity` →
entity object; `.financials / .market_data / .fillings` backed by canonical datasets, provenance-bound;
provider CI demo green.

**Phase 11 — Hardening, Testing, Docs** *· All hands* (E25/E26/E28)
Structured logging, error taxonomy wired everywhere, streaming/resumable sync, benchmarks; test-suite
split + integration e2e + CI coverage gate; security redaction/tamper tests; per-subsystem docs;
v1 acceptance (both core-success tests).

### Sequencing rules

- Phases 1–4 are the critical path; 1 and 3 are strictly blocking.
- Abdullah (security/acquisition) and Tasbiha (docs-site) run from day one in parallel.
- Ifra owns the quality stack (normalization → validation → metadata → entities) once schemas land
  (Phase 3+).
- Every task: an ID, one owner, a DoD, a PR.

### Definitions of done — v1 acceptance (summary)

See **E28**. The two non-negotiable green demos: (1) the core lifecycle on a local file with
provenance/lineage; (2) `resolve_company("AAPL").financials` returning a provenance-bound Dataset.

### Status legend

| Area | Checklist | Status |
|---|---|---|
| Core Dataset | E1 | **DONE** — Dataset + load/inspect/profile/save/export/conversions + Result + error taxonomy real |
| Acquisition | E2 | ~40% (`RawCache` + `Client` (retries/backoff/error mapping/streaming) real; pagination/sync/Source API pending) |
| Parsing | E3 | **DONE** — engine + csv/json/jsonl/parquet/xml parsers real |
| Schemas / Contracts | E4 | ~40% (Schema/FieldDef + 7 canonical schemas defined; registry + engines pending) |
| Normalization | E5 | **DONE** — engine + 17 rules real |
| Quality | E6 | ~60% (validate + 22 rules real; profile real; score model + check_* wrappers pending) |
| Metadata | E7 | ~60% (MetaData/ColumnMetadata/QualityInfo/InspectReport + profile/inspect real; get_metadata wrapper pending) |
| Provenance / Lineage | E8/E9 | ~25% (models + Dataset info methods real; automatic capture pending) |
| Entities | E10 | ~30% (Entity/EntityMatch/Resolver + countries/get_cik real; registry + resolve API pending) |
| Dataset Catalog | E11 | ~5% (stubs) |
| Storage / Query / Export | E12–15 | ~25% (export/utils + Dataset.save/export real; storage backends/query stubs) |
| Versioning / Migration | E16/E17 | ~10% (DataVersion model exists) |
| Public API + CLI | E20/E24 | ~50% (data API real: parse/normalize/validate/profile/inspect/freqs/ranges/anomalies; credentials real; Rust CLI subcommands parse but are unwired; fetch/schema/storage wrappers stubs) |
| Scheduler | — | **DONE** — cron/interval job scheduler in `hermes.core.scheduler` |
| Connectors on engine | Phase 9 | ~40% (9 connectors work with shared cache/client; GDELT is a stub; contract pending) |
| Provider layer | Phase 10 | ~5% (entities skeleton) |
| Hardening / Testing / Docs | E25/E26/E28 | ~35% (414 tests pass; docs being brought in line; platform hardening pending) |

---

## Part H — Positioning, Licensing & Credibility

### License — Elastic License 2.0 (decided)

Hermes is **source-available**, not OSI "open source", under **Elastic License 2.0 (ELv2)** — the same
family used by Elastic/Couchbase. Reasons:

- **Credibility:** a lawyer-drafted license instead of a hand-written one; terms are precise and
  defensible.
- **Honesty:** no false "open source" claims anywhere.
- **Protecting the cloud business:** ELv2 forbids offering the software to third parties as a hosted /
  managed service — only Hermes (via a commercial license) may host a "cloud Hermes".
- **Adoption-friendly:** individual/research/internal-commercial use, modification, and redistribution
  are free and unconditional (no employee/revenue counting).

**Monetization:** **Hermes Enterprise** — commercial license for support, SLAs, enterprise features,
and managed-hosting rights. Big organizations adopt the free engine; revenue comes from the Enterprise
edition and the cloud, not from the core license.

### Where Hermes competes

The vertical slice nobody owns: **trustworthy canonical datasets, with provenance, for finance &
defense, served through an entity-centric API** — resolve a company/country/person → on-demand canonical
datasets, gated by a ~100k-entity registry.

Integrate (never wrap): Polars, pandas, DuckDB, Arrow, PyArrow. Complement: dlt/Airbyte/Singer (use
their output). Integrate adapters later: Great Expectations, pandera, Splink/Dedupe (behind `Resolver`),
OpenLineage (export lineage to them), DVC/lakeFS (storage-level versioning).

Deliberately NOT building: BI dashboards, an ML framework, a generic ETL/DAG/orchestration system, HTML
report generation, a general tap ecosystem, a columnar database.

### The moat

| Candidate | Moat? | Why |
|---|---|---|
| Entity registry (finance/defense: companies/countries/persons) | **Strong** | a maintained, deduplicated ~100k-entity registry + aliases is a data asset competitors won't rebuild |
| Entity-centric data provider | **Strong once live** | the product's face; harder to switch, stronger lock-in |
| Canonical schemas (7 domains) | Strong, if maintained | few operate public versioned canonical schemas for finance/defense |
| Provenance + traceable normalization | Strong | auditable end-to-end normalization is what finance/defense buyers need |
| Connector breadth | Not a moat | dlt/airbyte out-source us 100:1 |
| Dataset-as-only-currency | Becoming moat | once Dataset is the only currency, datasets/resolvers/exports compose on it |

### Credibility strategy

The largest credibility risk was the gap between claims and code. That gap is being closed by: truthful
README, ELv2 license, CI on PRs, and the two CI-green success demos (engine vertical slice +
`resolve_company` provider demo). Reputation is measured by *external PRs merged, installs-to-works
time, reproduction hashes, time-to-first-useful-dataset* — not stars.

### Top 10 highest-leverage improvements

1. README/document truth pass + license repositioning **(in progress / mostly done)**
2. Local-file lifecycle real (parse→normalize→validate→Dataset→save→query→export)
3. CI-verified Dataset-first pipeline demo
4. Connector contract (`BaseConnector` + registry + shared acquisition)
5. Provenance/lineage recorded + persisted
6. Schema registry + validation over the 7 canonical schemas
7. CI gates PRs + coverage threshold
8. Live quickstart + honest roadmap on docs-site
9. Provider demo green (`resolve_company("AAPL").financials`)
10. ~100k-entity registry seeded (companies/countries/persons)

### NOW / NEXT / LATER / DON'T BUILD

**NOW (this month):** local-file lifecycle end-to-end + CI smoke test; provenance/lineage recorded at
ingest; CI gates PRs; connector retry/cache centralized in acquisition; README truth pass complete.

**NEXT (months 2–3):** BaseConnector + registry (World Bank reference wedge); schema registry + 7
canonical schemas + validation + contracts; storage backends + `Dataset.save/load/query`; entity
resolution real (Ifra); provider demo; feature layer removed or consolidated; changelog + semver.

**LATER (6–12 months):** DuckDB query engine; versioning/diff/snapshot; schema migration; `resolve`
provider layer live with ~100k entities (companies/countries/persons) and finance/defense datasets;
contributor surfaces; 2–3 case studies with reproducible hashes; OpenLineage/GX/pandera/Splink adapters.

**DON'T BUILD:** Hermes Cloud (waits for a real product); Healthcare/Trade/Energy/Climate domains until
finance/defense are proven; a tap-for-everything connector ecosystem (integrate dlt/Airbyte); BI /
dashboards / ML framework / orchestration / HTML report generators; a second (DAG) lineage architecture;
a giant universal schema; standalone feature engines on top of the current scope.

### First 5 actions (roadmap-linked)

1. **License — DONE (2026-09): ELv2** in `LICENSE.md`/`pyproject.toml`/README/docs-site; Enterprise =
   commercial path.
2. **Truth-fix README + root artifact** — README rewritten to "Implemented / Planned" (done); convert
   root `main.py` to a benchmark script (pending).
3. **Land the local-file core loop** as a CI-smoke-tested vertical slice (Phases 1–4).
4. **Wire provenance + lineage as recorded facts at ingest**, persisted with the Dataset,
   exposed via `provenance_info/lineage_info`.
5. **Make CI gate PRs** — `tests.yml` on `pull_request`, coverage threshold, honest workflow names,
   docs-site version synced to the package version.

---

*Everything else depends on the engine lifecycle and the entity-centric provider demo being real first.*