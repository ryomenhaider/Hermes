# Hermes

> Universal data acquisition and feature engineering SDK for intelligence, finance, and defense applications.

Hermes fetches data from 40+ free global sources, normalizes it, engineers intelligence-ready features, and exposes everything through a clean Python interface (with CLI and TUI). It is **not** an API server — it is an SDK you import, run, and own.

```text
pip install hermes-plt
# or
uv add hermes-plt
```

---

## Quickstart

```python
from hermes import Hermes

hr = Hermes()

# FRED — US macro data (free key required)
fred_api = hr.fred.connect("YOUR_API_KEY")
gdp = hr.fred.get_series("GDP", api=fred_api)

# World Bank — no key needed
china_gdp = hr.world_bank.get_indicator("NY.GDP.MKTP.CD", country="CHN")

# IMF — no key needed
imf_data = hr.imf.get_data("IFS", country="US", indicator="NGDP_XDC")

# GDELT — no key needed
events = hr.gdelt.query_events(
    countries=["UKR", "RUS"],
    themes=["CONFLICT", "MILITARY"],
    start_date="2024-01-01",
)

# Feature engineering
from hermes.features import FeatureEngineer
fe = FeatureEngineer()
risk = fe.build_country_risk_features(country="UKR", date="2026-07-14")
```

Every connector returns a **pandas DataFrame**. Optional `export=True` saves to JSON, CSV, Parquet, or Pickle.

---

## Interfaces

| Interface | Command | Purpose |
|---|---|---|
| **Python SDK** | `from hermes import Hermes` | Primary interface |
| **CLI** | `$ hermes fetch <source> <indicator>` | Scripting, automation |
| **TUI** | `$ hermes tui` | Terminal dashboard |

```text
$ hermes fetch fred GDP --country USA --start 2020-01-01
$ hermes fetch world-bank NY.GDP.MKTP.CD --country CHN
$ hermes features build --country UKR --output risk_features.parquet
$ hermes connectors list
$ hermes cache clear --older-than 7d
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              HERMES SDK                                     │
│                    from hermes import Hermes                                │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                         CONNECTOR LAYER                               │  │
│  │  FRED  World Bank  IMF  GDELT  NewsAPI  UN Comtrade  BIS  OECD  ...   │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                   ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      CORE / CLEANING LAYER                            │  │
│  │  • Schema normalization (ISO dates, ISO country codes, USD values)    │  │
│  │  • Missing value handling (forward-fill, interpolation)               │  │
│  │  • Frequency alignment (D → M → Q → A)                                │  │
│  │  • Outlier detection (IQR, Z-score, MAD)                              │  │
│  │  • Deduplication (hash-based + fuzzy)                                 │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                   ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                   FEATURE ENGINEERING LAYER                           │  │
│  │  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────────────┐  │  │
│  │  │     Economic     │ │  Geopolitical   │ │       Composite        │  │  │
│  │  │   • Growth       │ │   • Conflict    │ │  • Country Risk Score  │  │  │
│  │  │   • Volatility   │ │   • Diplomatic  │ │  • Financial Stress    │  │  │
│  │  │   • Inflation    │ │   • Protest     │ │  • Supply Chain Vuln.  │  │  │
│  │  │   • External     │ │   • Governance  │ │  • Social Stability    │  │  │
│  │  └─────────────────┘ └─────────────────┘ └─────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                   ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                   STORAGE & METADATA LAYER                            │  │
│  │  Raw Cache (Parquet) · Feature Store · Metadata Registry · Lineage    │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                                   ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                      USER INTERFACES                                  │  │
│  │        Python SDK (Primary)    CLI    TUI (Terminal Dashboard)        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Feature Engineering

Hermes transforms raw connector output into intelligence-ready features through a declarative pipeline. Features are versioned, cached, and documented in the metadata registry.

### Economic

| Category | Examples | Input Sources | Output Use |
|---|---|---|---|
| Growth | GDP YoY/QoQ, industrial production growth | FRED, WB, IMF | Risk scoring, forecasting |
| Volatility | Rolling std (12m), max drawdown, CV | FRED, IMF | Anomaly detection |
| Stress | Credit spread, yield curve inversion | FRED, BIS | Financial risk |
| External | Current account/GDP, FX reserves, debt/GDP | WB, IMF | Sovereign risk |
| Inflation | CPI YoY, PPI, hyperinflation flag | FRED, WB | Monetary stability |
| Labor | Unemployment, youth unemployment | FRED, WB, OECD | Social stability |

### Geopolitical

| Category | Examples | Input Sources | Output Use |
|---|---|---|---|
| Conflict | Event count, Goldstein scale, battle deaths | GDELT, UCDP | Security risk |
| Diplomatic | Treaty signings, diplomatic expulsions | GDELT | Political risk |
| Protest | Event count, violence level, spread | GDELT | Social stability |
| Governance | WGI composite, corruption, rule of law | WB, V-DEM | Institutional risk |
| Media | News sentiment, narrative shift velocity | NewsAPI, GDELT GKG | Trend analysis |

---

## Sources

### Build Order

| Prio | Connector | Key Required | Aegis Uses | Atlas Uses |
|---|---|---|---|---|
| W1 | FRED | Free (any email) | Economic risk, forecasting | Macro context |
| W1 | World Bank | None | GDP, poverty, governance | Country properties |
| W2 | IMF | None | Financial stats, BOP, WEO | Financial context |
| W3 | BIS | None | Banking stress, credit | Financial institutions |
| W3 | UN Comtrade | Free (any email) | Trade flows, sanctions | Trade relationships |
| W4 | GDELT | None | Conflict, protest, events | Event / actor nodes |
| W4 | UCDP | None | Armed conflict baseline | Conflict nodes |
| W5 | NewsAPI | Free (any email) | RAG, sentiment, trends | Entity extraction |
| W5 | FAO | None | Food security, prices | Commodity nodes |
| W6 | OECD | None | Policy, tax, trade | Policy context |
| W6 | Eurostat | None | EU economic data | EU country properties |
| W7 | EIA | Free (any email) | Energy prices, production | Energy nodes |
| W7 | IEA | Free account | Energy dependence | Energy relationships |
| W8 | USGS | None | Minerals, earthquakes | Mineral / location nodes |
| W8 | V-DEM | Free download | Democracy, regime type | Governance edges |
| W9 | Freedom House | Free download | Political rights | Freedom properties |
| W9 | Transparency Int. | Free download | Corruption index | Corruption properties |
| W10 | ND-GAIN | None | Climate vulnerability | Climate risk properties |
| W10 | EM-DAT | Free account | Natural disasters | Disaster event nodes |
| W11 | NASA POWER | None | Climate data | Environmental context |
| W11 | Open-Meteo | None | Weather, forecasts | Agricultural risk |
| W12 | Wikidata | None | Entity resolution | Entity enrichment |
| W12 | OpenStreetMap | None | Geocoding, boundaries | Location nodes |

### Complete Inventory (40+ sources)

**Economic & Financial** — FRED ✅ · World Bank ✅ · IMF · BIS · UN Comtrade · OECD · Eurostat · Penn World Table · Maddison Project · CEPII

**Geopolitical & Conflict** — GDELT · UCDP · PRIO / Prio Grid · Correlates of War · SIPRI Arms Transfers · Polity IV / V-DEM · CIRI Human Rights · Freedom House · Transparency International · Reporters Without Borders · Fragile States Index · Fund for Peace

**Environmental, Social & Commodity** — FAO · IEA · EIA · USGS · ND-GAIN · EM-DAT · NASA POWER · Open-Meteo · Our World in Data · UN Data

**Media, Knowledge & Geospatial** — NewsAPI · GDELT GKG · Wikidata · Wikipedia API · OpenStreetMap · Natural Earth · Sentinel Hub · OpenCorporates

All sources are free to access. None require an institutional (.edu/.org/.gov) email.

---

## License

MIT
