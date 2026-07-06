# Hermes

> The foundational intelligence data platform.

Hermes is a production-grade data platform responsible for acquiring, validating, normalizing, storing, and serving intelligence datasets.

It serves as the single source of truth for all downstream intelligence systems by transforming heterogeneous external datasets into a unified, reliable, versioned, and queryable internal representation.

Hermes is the data foundation of the intelligence ecosystem.

---

# Overview

Intelligence-relevant data is fragmented across numerous providers, formats, and delivery mechanisms.

Examples include:

* ACLED conflict and protest events
* GDELT global event streams
* World Bank economic indicators
* IMF macroeconomic indicators
* OFAC sanctions data
* FRED financial indicators
* SIPRI defense and military expenditure data
* UN Comtrade trade statistics

Each source introduces unique challenges:

* Different schemas
* Different identifiers
* Different update frequencies
* Different quality standards
* Different ingestion methods

Without a centralized platform, every downstream application must repeatedly implement:

* Data acquisition
* Data cleaning
* Data validation
* Schema normalization
* Data storage
* Source integration

Hermes centralizes these responsibilities and exposes a consistent internal data model.

---

# Mission

Provide a unified, reliable, auditable, and scalable intelligence data platform.

---

# Architectural Role

```text
External Sources
        │
        ▼
      Hermes
        │
        ▼
      Aegis
        │
        ▼
      Atlas
        │
        ▼
   Applications
```

Hermes is responsible only for data management.

It does not perform analytics, forecasting, machine learning, or risk assessment.

---

# Core Responsibilities

## 1. Data Acquisition

Hermes acquires datasets from external providers.

Supported ingestion methods include:

* REST APIs
* Bulk downloads
* CSV exports
* JSON feeds
* XML feeds

Acquisition capabilities include:

* Authentication
* Pagination
* Rate limiting
* Retry handling
* Download orchestration
* Incremental synchronization

---

## 2. Data Validation

All incoming data is validated before storage.

Validation examples:

* Required field verification
* Timestamp validation
* Country code validation
* Numeric range validation
* Duplicate detection
* Referential integrity checks

Invalid records may be:

* Rejected
* Quarantined
* Logged for investigation

---

## 3. Data Normalization

Hermes converts source-specific schemas into canonical internal schemas.

### Example

Source schema:

```json
{
  "event_id_cnty": "123",
  "event_date": "2026-01-01"
}
```

Canonical Hermes schema:

```json
{
  "event_id": "123",
  "occurred_at": "2026-01-01"
}
```

Downstream systems interact only with canonical Hermes models.

---

## 4. Data Storage

Hermes persists normalized datasets in structured storage systems.

### Current Storage

* PostgreSQL

### Future Storage Targets

* Parquet datasets
* Object storage
* Data lake architectures

Storage requirements:

* Queryable
* Versioned
* Auditable
* Reliable
* Transactional

---

## 5. Metadata Management

Hermes tracks operational and lineage metadata for every ingestion process.

Examples include:

* Synchronization history
* Processing duration
* Dataset versions
* Failure rates
* Record counts
* Connector versions

Every ingestion operation must be traceable.

---

## 6. Data Serving

Hermes exposes normalized datasets through APIs.

Consumers never interact directly with external providers.

All access flows through Hermes.

Benefits include:

* Consistent schemas
* Stable interfaces
* Centralized governance
* Improved reliability

---

# Non-Responsibilities

Hermes intentionally does **not** perform:

* Risk scoring
* Country ranking
* Forecast generation
* Machine learning training
* Machine learning inference
* LLM inference
* Knowledge graph analytics
* Dashboard rendering
* Strategic assessment

These responsibilities belong to downstream systems.

---

# Data Domains

## Events

Intelligence-relevant occurrences.

Examples:

* Protests
* Riots
* Armed conflict
* Political violence

Sources:

* ACLED
* GDELT

---

## Economics

Macroeconomic and financial indicators.

Examples:

* GDP
* Inflation
* Debt
* Unemployment

Sources:

* IMF
* World Bank
* FRED

---

## Trade

International trade activity.

Examples:

* Imports
* Exports
* Trade balances

Sources:

* UN Comtrade

---

## Sanctions

Sanctions and enforcement information.

Examples:

* Entity sanctions
* Country sanctions
* Enforcement actions

Sources:

* OFAC

---

## Defense

Defense and military indicators.

Examples:

* Military expenditure
* Arms transfers
* Defense budgets

Sources:

* SIPRI

---

# Canonical Data Philosophy

Hermes standardizes all external data into canonical schemas.

A canonical schema is the internal representation used regardless of source origin.

### Example

Source A:

```json
{
  "country": "Pakistan"
}
```

Source B:

```json
{
  "nation": "Pakistan"
}
```

Canonical representation:

```json
{
  "country_name": "Pakistan"
}
```

This ensures downstream consumers operate on a consistent data model.

---

# Connector Architecture

Every external source is isolated behind a dedicated connector.

```text
connectors/

├── acled/
├── gdelt/
├── world_bank/
├── imf/
├── ofac/
├── fred/
├── sipri/
└── un_comtrade/
```

Each connector is responsible for:

* Fetching data
* Validating source payloads
* Mapping to canonical schemas
* Persisting normalized records

Connectors are independently developed and maintained.

---

# Internal Architecture

## Connector Layer

Handles communication with external systems.

Responsibilities:

* API interaction
* Authentication
* Download management
* Synchronization orchestration

---

## Validation Layer

Enforces data quality standards.

Responsibilities:

* Schema validation
* Constraint validation
* Duplicate detection
* Data integrity checks

---

## Mapping Layer

Normalizes source-specific structures.

Responsibilities:

* Schema conversion
* Field mapping
* Type conversion
* Canonical transformation

---

## Storage Layer

Persists normalized datasets.

Responsibilities:

* Database interaction
* Transactions
* Version management
* Persistence operations

---

## Metadata Layer

Tracks operational information and lineage.

Responsibilities:

* Run history
* Dataset lineage
* Audit records
* Data provenance

---

## API Layer

Provides access to stored datasets.

Responsibilities:

* Query interfaces
* Filtering
* Pagination
* Data retrieval

---

# Core Entities

## Country

Represents sovereign entities.

Examples:

* Pakistan
* India
* China

---

## Event

Represents intelligence-relevant occurrences.

Examples:

* Protest
* Conflict
* Riot

---

## Indicator

Represents measurable metrics.

Examples:

* GDP
* Inflation
* Debt

---

## TradeRecord

Represents trade activity.

Examples:

* Imports
* Exports

---

## SanctionRecord

Represents sanctions-related information.

Examples:

* Entity sanctions
* Country sanctions

---

# Dataset Lineage

Hermes maintains full lineage tracking.

Each record should retain:

* Source system
* Source identifier
* Connector version
* Ingestion timestamp
* Processing run identifier
* Dataset version
* Record origin metadata

Every stored record must be traceable back to its source.

---

# Observability

Hermes continuously monitors platform health.

Metrics include:

* Connector failures
* Synchronization duration
* Records processed
* Records rejected
* Data freshness
* API performance
* Storage utilization

Observability enables reliable operations and rapid issue detection.

---

# Reliability Requirements

Hermes is designed for resilient data operations.

Requirements include:

* Retry mechanisms
* Idempotent ingestion
* Duplicate protection
* Transactional writes
* Failure recovery
* Fault isolation
* Auditability

---

# Scalability Requirements

Hermes must scale without architectural redesign.

The platform should support:

* Additional connectors
* Additional datasets
* Increased ingestion volume
* Increased storage volume
* Multiple downstream consumers
* Future storage backends

---

# Long-Term Vision

Hermes serves as the intelligence data backbone for the broader ecosystem.

Future platforms should consume data exclusively through Hermes, including:

* Aegis
* Atlas
* Aion
* Internal analytics systems
* Research platforms
* Decision-support tools

By centralizing acquisition, validation, normalization, storage, and serving, Hermes ensures that data infrastructure is implemented once and reused everywhere.

---

# Guiding Principle

> Acquire once. Normalize once. Validate once. Serve everywhere.
