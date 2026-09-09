# Hermes

### The Data Engine for Python

**Fetch. Parse. Normalize. Validate. Profile. Transform. Query. Export.**

Hermes is an open source, Python native data engine designed to make working with external and existing datasets dramatically easier.

Instead of writing a different pipeline for every API, CSV, JSON response, database, or public dataset, Hermes provides one consistent system for bringing data in, understanding it, cleaning it, validating it, transforming it, and making it ready for analysis and machine learning.

```python
import hermes as hr

data = hr.fetch("world_bank", dataset="gdp")

data = data.parse()
data = data.normalize()
data = data.validate()

print(data.profile())

df = data.to_polars()
```

Hermes is built around a simple idea:

> **Data should be as easy to work with as the models and applications built on top of it.**

---

# Why Hermes?

Modern data work is full of repetitive engineering.

Every new source means dealing with different APIs, authentication methods, formats, schemas, naming conventions, missing values, types, timestamps, units, identifiers, duplicates, and validation rules.

The result is usually the same pattern repeated across hundreds of projects:

```text
Fetch
Clean
Rename
Cast
Validate
Deduplicate
Normalize
Save
Repeat
```

Hermes turns that repeated work into reusable infrastructure.

```python
data = hr.fetch(source)

data = data.parse()
data = data.normalize()
data = data.validate()

data.profile()
data.inspect()

data.save("my_dataset")
```

The goal is not to replace Pandas, Polars, DuckDB, PyArrow, or other excellent tools.

The goal is to make them easier to use together.

---

# What Hermes Is

Hermes is a general purpose data lifecycle engine.

It provides a common system for:

* Acquiring data
* Parsing raw data
* Inferring schemas
* Defining schemas
* Normalizing data
* Converting types
* Converting units
* Aligning timestamps
* Cleaning datasets
* Validating data
* Profiling datasets
* Detecting anomalies
* Detecting duplicates
* Transforming data
* Resolving entities
* Versioning datasets
* Tracking provenance
* Tracking lineage
* Querying datasets
* Storing datasets
* Loading datasets
* Exporting datasets

The same core system can work with completely different domains.

Finance.

Defense.

Healthcare.

Trade.

Energy.

Climate.

Geopolitics.

Research.

Enterprise data.

Private datasets.

The core does not need to understand every domain.

Domain specific knowledge can be added on top.

---

# The Hermes Ecosystem

Hermes Core provides the general data engine.

Additional Hermes packages provide specialized capabilities.

```text
Hermes Core
    |
    + Hermes Finance
    |
    + Hermes Defense
    |
    + Hermes Healthcare
    |
    + Hermes Trade
    |
    + Hermes Energy
    |
    + Hermes Climate
    |
    + Hermes Geopolitics
    |
    + Hermes Corporate
    |
    + Hermes Entity
    |
    + Hermes Features
    |
    + Hermes Connectors
```

This allows Hermes to remain small and general while the ecosystem grows around it.

A developer working with financial data should not need to install defense infrastructure.

A developer working with healthcare data should not need the finance package.

The core remains universal.

The ecosystem becomes specialized.

---

# The Core API

Hermes is designed around a small, understandable API.

| Function        | Purpose                                        |
| --------------- | ---------------------------------------------- |
| `fetch()`       | Retrieve data from an external source          |
| `ingest()`      | Bring an existing dataset into Hermes          |
| `parse()`       | Convert raw data into structured records       |
| `normalize()`   | Convert data into a consistent representation  |
| `validate()`    | Verify that data satisfies defined rules       |
| `profile()`     | Analyze the structure and quality of a dataset |
| `inspect()`     | Explore data, schema, metadata and quality     |
| `transform()`   | Apply transformations to data                  |
| `resolve()`     | Connect records to canonical entities          |
| `deduplicate()` | Detect and handle duplicate records            |
| `query()`       | Query Hermes datasets                          |
| `save()`        | Persist datasets                               |
| `load()`        | Load datasets                                  |
| `export()`      | Export data to other systems                   |
| `snapshot()`    | Create an immutable dataset version            |
| `diff()`        | Compare dataset versions                       |
| `metadata()`    | Retrieve dataset information                   |
| `lineage()`     | Show how data was produced                     |
| `provenance()`  | Show where data came from                      |

The API is intentionally composable.

```python
dataset = hr.fetch("source")

dataset = dataset.parse()
dataset = dataset.normalize()
dataset = dataset.validate()

dataset.profile()
dataset.inspect()

dataset.save("dataset")
```

---

# Fetch Anything

Hermes provides a common interface for acquiring external data.

```python
data = hr.fetch("world_bank", dataset="gdp")
```

The source can eventually be anything supported by a Hermes connector.

APIs.

Bulk downloads.

CSV files.

JSON.

XML.

Parquet.

Databases.

Data streams.

Custom sources.

The connector handles communication with the source.

Hermes Core handles what happens after the data arrives.

---

# Ingest Existing Data

Not every dataset comes from an API.

Hermes can ingest datasets that already exist.

```python
data = hr.ingest("dataset.parquet")
```

```python
data = hr.ingest("dataset.csv")
```

```python
data = hr.ingest("dataset.json")
```

The same Hermes lifecycle can then be applied.

```python
data.profile()
data.validate()
data.normalize()
data.save("my_dataset")
```

---

# Parse

Raw data should not immediately become a final dataset.

Hermes separates acquisition from interpretation.

```python
data = hr.fetch(source)

structured = data.parse()
```

Parsing deals with the representation of the source.

JSON becomes records.

CSV becomes records.

XML becomes records.

Compressed archives become usable data.

Source specific parsing logic remains inside the appropriate parser.

---

# Normalize

Different sources rarely describe data in exactly the same way.

One source might use:

```text
country
```

Another:

```text
country_name
```

Another:

```text
CountryName
```

Another:

```text
location
```

Hermes provides a normalization layer that can map these different representations into consistent schemas.

```python
data = data.normalize()
```

Normalization can handle:

* Names
* Types
* Dates
* Timezones
* Units
* Currencies
* Country codes
* Identifiers
* Categories
* Frequencies
* Source specific representations

The goal is simple:

> **Different sources should become easier to use together.**

---

# Validate

Hermes does not assume that data is correct just because it successfully downloaded.

```python
report = data.validate()
```

Validation can check:

* Required fields
* Data types
* Missing values
* Invalid values
* Duplicate records
* Identifier validity
* Date consistency
* Range constraints
* Schema compatibility
* Referential integrity
* Domain specific rules

Validation results remain inspectable.

```python
report.valid
report.errors
report.warnings
```

---

# Profile

Before working with a dataset, you should be able to understand it immediately.

```python
profile = data.profile()
```

Hermes can provide information such as:

```text
Rows
Columns
Types
Missing values
Unique values
Duplicates
Value ranges
Distributions
Date ranges
Frequency
Schema
Quality checks
```

The objective is simple:

> **Open a dataset and understand what you are dealing with.**

---

# Inspect

Hermes provides a higher level inspection interface for developers.

```python
data.inspect()
```

Inspection can expose:

* Dataset information
* Schema
* Sample records
* Metadata
* Validation results
* Profile
* Quality information
* Source
* Lineage
* Version
* Entity information

A dataset should not be a black box.

---

# Transform

Hermes should work with the tools developers already use.

```python
data = data.transform(my_function)
```

Complex transformations can be composed into pipelines.

```python
data = data.transform(clean_dates).transform(calculate_features).transform(remove_invalid_records)
```

Hermes does not try to become another dataframe library.

Instead, it provides the pipeline layer around existing data tools.

---

# Entity Resolution

Data from different sources often refers to the same real world entity in different ways.

Hermes provides an interface for connecting those records.

```python
data = data.resolve()
```

For example:

```text
Apple Inc.
Apple Computer Inc.
Apple Computer, Inc.
AAPL
US0378331005
```

can potentially be connected to a canonical entity.

The actual resolution logic can come from specialized Hermes packages.

This allows the same infrastructure to support:

* Companies
* Countries
* Securities
* Organizations
* Locations
* Vessels
* Other domain specific entities

---

# Dataset Versioning

Data changes.

Sources revise historical values.

Schemas change.

Pipelines improve.

Hermes treats datasets as evolving objects.

```python
dataset.snapshot()
```

```python
dataset.version()
```

```python
dataset.diff("v1", "v2")
```

This makes it possible to understand what changed between dataset versions.

Historical data should remain reproducible instead of silently changing underneath your application.

---

# Provenance

Every dataset should answer:

> Where did this data come from?

Hermes keeps provenance information alongside the dataset.

For example:

```python
dataset.provenance()
```

could return:

```text
WorldBank
parser@1.3.0
mapper@0.9.3
normalizer@1.4.7
validator@3.4.8
dataset@gdp_v2
```

A much more complex system can eventually be built on top of this.

The foundation remains simple.

---

# Lineage

Hermes records how data moves through the system.

For example:

```text
WorldBank
    ↓
Parser
    ↓
Mapper
    ↓
Normalizer
    ↓
Validator
    ↓
Entity Resolver
    ↓
Dataset
```

The important thing is that the final dataset is not disconnected from the process that produced it.

Developers should be able to trace data back through the pipeline.

---

# Works With Your Data Stack

Hermes is designed to work with the Python data ecosystem.

Potential integrations include:

| Tool                        | Hermes Integration        |
| --------------------------- | ------------------------- |
| Pandas                      | DataFrame conversion      |
| Polars                      | DataFrame conversion      |
| PyArrow                     | Arrow data interchange    |
| DuckDB                      | Analytical querying       |
| NumPy                       | Numerical processing      |
| Parquet                     | Dataset storage           |
| SQL databases               | Data ingestion and export |
| Machine learning frameworks | ML ready datasets         |

Hermes should make existing tools work together rather than force developers into a proprietary data model.

---

# Connectors

Hermes connectors provide access to external sources.

A connector should primarily answer:

> How do I get this source's data?

Hermes Core handles the rest.

A connector can provide:

* Authentication
* Requests
* Pagination
* Rate limiting
* Retries
* Source specific parsing
* Source metadata

Connectors can be independently developed and distributed.

This allows the ecosystem to grow without constantly changing Hermes Core.

---

# Domain Packages

Hermes Core provides the infrastructure.

Domain packages provide knowledge.

For example:

### Hermes Finance

Financial datasets, securities, companies, economic indicators, market data, financial statements and financial features.

### Hermes Defense

Defense expenditure, conflicts, military organizations, equipment, arms transfers, security events and defense indicators.

### Hermes Healthcare

Healthcare statistics, diseases, organizations, hospitals, medicines and public health datasets.

### Hermes Trade

Trade flows, commodities, customs information, ports, countries and supply chain datasets.

The same core engine can power all of them.

---

# Feature Engineering

Hermes can also provide reusable feature engineering through specialized packages.

For example:

```python
features = finance.features(data)
```

or:

```python
features = defense.features(data)
```

Features should have explicit definitions and dependencies.

This makes them reusable across research, analytics and machine learning systems.

---

# Designed for Developers

Hermes should feel natural in Python.

```python
import hermes as hr

dataset = hr.fetch("source")

dataset = dataset.parse().normalize().validate()

dataset.profile()

df = dataset.to_polars()
```

No giant framework is required to get started.

No forced cloud account.

No mandatory hosted service.

No requirement to use a proprietary storage system.

Hermes Core is open source.

---

# Local First

Hermes is designed to work locally.

A developer should be able to:

```text
pip install hermes-plt
```

and start working with data immediately.

Local files can be used.

Local storage can be used.

DuckDB can be used.

Parquet can be used.

Polars can be used.

A database can be added when the project needs one.

Cloud infrastructure should be an extension of Hermes, not a requirement for using it.

---

# Built for Growth

Hermes starts small.

A single developer can use it for a single dataset.

A research team can use it for hundreds of datasets.

A company can build internal data pipelines around it.

Larger deployments can eventually introduce:

* Remote datasets
* Distributed processing
* Object storage
* Dataset catalogs
* Continuous ingestion
* Hosted APIs
* Large scale querying
* Team access
* Enterprise controls

The same core concepts remain intact.

---

# What Hermes Is Not

Hermes Core is not trying to be:

* A replacement for Pandas
* A replacement for Polars
* A replacement for DuckDB
* A data warehouse
* A machine learning framework
* A dashboarding platform
* An intelligence application
* A knowledge graph by itself
  
Hermes exists to sit between **data sources and the applications that depend on that data**.

---

# Philosophy

### Data should be composable

A dataset from one source should be usable alongside a dataset from another source.

### Data should be inspectable

Developers should know what they received before building on it.

### Data should be reproducible

The same pipeline should be understandable and repeatable.

### Data should be traceable

Every important dataset should have a clear origin.

### Data should be interoperable

Hermes should work with the ecosystem instead of locking developers into Hermes.

### Data infrastructure should be reusable

The same ingestion, validation and transformation infrastructure should work across domains.

---

# Roadmap

## Phase 1

Hermes Core foundation.

* Fetch
* Ingest
* Parse
* Normalize
* Validate
* Profile
* Inspect
* Transform
* Export
* Dataset abstraction
* Connector system
* Schema system

## Phase 2

Reliable data infrastructure.

* Dataset storage
* Dataset versions
* Snapshots
* Provenance
* Lineage
* Better validation
* Better profiling
* Caching
* Query interface

## Phase 3

Ecosystem.

* Hermes Finance
* Hermes Defense
* Hermes Healthcare
* Hermes Trade
* Hermes Energy
* Hermes Climate
* Hermes Geopolitics
* Hermes Corporate
* Hermes Entity
* Hermes Features

## Phase 4

Scale.

* Remote datasets
* Object storage
* Distributed processing
* Continuous ingestion
* Large dataset querying
* Cloud execution

## Phase 5

Hermes Cloud.

A managed infrastructure layer built around Hermes Core.

* Hosted datasets
* APIs
* Dataset catalogs
* Continuous pipelines
* Versioned data
* Team access
* Usage controls
* Enterprise infrastructure

---

# The Vision

Hermes starts as a Python library.

It can grow into a complete ecosystem for data.

The long term goal is simple:

> **Make high quality data infrastructure accessible through one consistent developer experience.**

Instead of every developer building their own ingestion system.

Instead of every company rebuilding the same normalization pipelines.

Instead of every project implementing its own validation framework.

Instead of datasets becoming disconnected collections of files.

Hermes provides the common foundation.

**One engine.**

**One ecosystem.**

**Any data.**

---

# Contributing

Hermes is open source and built for developers.

Contributions can include:

* Connectors
* Parsers
* Normalizers
* Validators
* Profilers
* Storage backends
* Query integrations
* Domain packages
* Documentation
* Testing
* Performance improvements

Build something useful.

Share it.

Improve it.

Build on top of it.

---

# License

[License information will be added here.]

---

# Hermes

**The data engine for the Python ecosystem.**

**Bring the data in. Make it usable. Know where it came from. Build on it.**
