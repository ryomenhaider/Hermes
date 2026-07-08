# Hermes - Universal Data Acquisition Platform

## Vision

Hermes is a terminal-first data acquisition platform that allows developers, analysts, researchers, intelligence teams, and data engineers to retrieve, validate, normalize, transform, and export data from hundreds of public and private data sources through a unified interface.

Instead of learning dozens of APIs, authentication methods, schemas, pagination systems, and export formats, users interact with a single platform.

Hermes acts as a universal connector layer between external data providers and user-defined destinations.

---

# Core Objective

Allow a user to:

1. Discover a data source
2. Authenticate once
3. Configure query parameters
4. Retrieve data
5. Validate data
6. Normalize schemas
7. Transform records
8. Export data anywhere

without writing custom integration code.

---

# Primary Users

## Data Engineers

Need reliable ingestion pipelines.

Examples:

* FRED → PostgreSQL
* World Bank → Snowflake
* SEC EDGAR → Parquet

---

## Financial Analysts

Need economic and market data.

Examples:

* CPI
* GDP
* Treasury Rates
* Exchange Rates

---

## Intelligence Analysts

Need OSINT and threat intelligence.

Examples:

* OpenSanctions
* VirusTotal
* OTX
* Shodan
* Open Ownership

---

## Researchers

Need structured datasets without dealing with APIs.

Examples:

* Conflict databases
* Economic indicators
* Geospatial datasets

---

# Product Philosophy

Hermes is not a dashboard.

Hermes is not a visualization tool.

Hermes is not a BI platform.

Hermes focuses exclusively on:

* Data acquisition
* Data standardization
* Data delivery

---

# High-Level Architecture

User
↓
Hermes TUI
↓
Source Registry
↓
Connector Engine
↓
Validation Engine
↓
Transformation Engine
↓
Export Engine
↓
Destination

---

# Major Components

## 1. Hermes TUI

Purpose:

Provide a modern terminal application for interacting with all data sources.

Technology:

* Textual

Responsibilities:

* Source discovery
* Search
* Authentication management
* Query building
* Export configuration
* Job monitoring

---

## 2. Source Registry

Purpose:

Maintain metadata for every available connector.

Stores:

* Source name
* Category
* Description
* Required credentials
* Available parameters
* Supported outputs

Example:

FRED

Category:
Finance

Credentials:
API Key

Parameters:
Series ID
Start Date
End Date
Limit

---

## 3. Connector Engine

Purpose:

Interact with external APIs and datasets.

Responsibilities:

* Authentication
* Request generation
* Pagination
* Rate limiting
* Retry logic
* Data retrieval

Examples:

* FRED Connector
* IMF Connector
* VirusTotal Connector
* SIPRI Connector

---

## 4. Validation Engine

Purpose:

Ensure incoming data is usable.

Checks:

* Required fields
* Type consistency
* Null handling
* Duplicate detection
* Schema verification

Technology:

* Pydantic

---

## 5. Transformation Engine

Purpose:

Convert source-specific data into standardized schemas.

Examples:

FRED GDP

{
"value": 29384
}

World Bank GDP

{
"GDP": 29384
}

Normalized Output

{
"gdp": 29384
}

Responsibilities:

* Field mapping
* Type conversion
* Renaming
* Flattening
* Normalization

---

## 6. Export Engine

Purpose:

Deliver processed data to target destinations.

Supported Outputs:

Files

* CSV
* JSON
* JSONL
* Excel
* Parquet

Databases

* PostgreSQL
* MySQL
* SQLite
* DuckDB
* MSSQL

Cloud Storage

* S3
* Azure Blob
* Google Cloud Storage

Data Warehouses

* Snowflake
* BigQuery
* Redshift

---

## 7. Credential Manager

Purpose:

Securely store authentication credentials.

Technology:

* keyring

Stores:

* API keys
* Tokens
* Usernames
* Passwords

Never stores secrets in plaintext.

---

## 8. Job Engine

Purpose:

Track all executions.

Stores:

* Job ID
* Source
* Parameters
* Status
* Runtime
* Records processed

Statuses:

* Pending
* Running
* Success
* Failed

---

## 9. Local Metadata Database

Purpose:

Store Hermes operational data.

Technology:

SQLite

Stores:

* Sources
* Saved Queries
* Export Targets
* Job History
* Connector Metadata

Does NOT store user datasets.

---

# Source Categories

## Finance & Economics

Macroeconomic

* FRED
* World Bank
* IMF
* ECB
* US Treasury

Markets

* Alpha Vantage
* CoinGecko
* ExchangeRate.host
* Financial Modeling Prep

Corporate Intelligence

* SEC EDGAR
* OpenCorporates
* Open Ownership
* Companies House

---

## Defense & Geopolitics

Conflict Data

* UCDP
* Correlates of War
* ICEWS
* GDELT
* Phoenix

Military Data

* SIPRI Arms
* SIPRI Military Expenditure
* NATO Data
* WMEAT

Geospatial

* NASA FIRMS
* NOAA
* USGS
* OpenStreetMap
* Copernicus

---

## Intelligence & OSINT

Entity Intelligence

* Wikidata
* DBpedia
* OpenSanctions
* Open Ownership
* LittleSis

Cyber Intelligence

* VirusTotal
* OTX
* AbuseIPDB
* URLHaus
* MalwareBazaar
* ThreatFox
* NVD
* GreyNoise

Transportation Intelligence

* OpenSky
* ADS-B Exchange
* MarineTraffic
* AISHub
* OurAirports

---

# User Experience

First Launch

Hermes asks:

1. Which sources do you plan to use?
2. Which credentials are required?
3. Validate credentials
4. Save securely

Subsequent Launches

User sees:

Search Sources

or

Browse Categories

Select Source

Fill Parameters

Choose Destination

Execute

Receive Data

---

# Search System

Primary navigation method.

Example:

Search:
fred

Results:
FRED Economic Data

Search:
virus

Results:
VirusTotal

Search:
gdp

Results:
FRED
World Bank
IMF

Users should not need to remember category hierarchies.

---

# Connector Standard

Every connector must implement:

authenticate()

validate_credentials()

fetch()

validate()

transform()

export()

health_check()

Connector outputs must return standardized Hermes DataFrames.

---

# Future Plugin System

Hermes must support external connectors.

Example:

pip install hermes-fred

pip install hermes-virustotal

pip install hermes-worldbank

The core platform automatically discovers and registers them.

---

# Future Features

Phase 2

* Scheduled jobs
* Background execution
* Incremental syncs
* Local caching
* Query templates

Phase 3

* REST API
* Web UI
* Team workspaces
* Shared credentials
* Audit logs

Phase 4

* AI-powered query generation
* Natural language data requests
* Automatic schema mapping
* Data quality scoring

---

# Non-Goals

Hermes will not:

* Build dashboards
* Create visualizations
* Replace Power BI
* Replace Tableau
* Replace Grafana
* Act as a data warehouse

Hermes focuses exclusively on data acquisition, normalization, and delivery.

---

# Success Definition

A developer should be able to install Hermes, authenticate once, select a source, configure a query, and export clean structured data to a file, database, or cloud destination in under five minutes without reading source-specific API documentation.
