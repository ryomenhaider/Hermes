from __future__ import annotations

import importlib
import inspect
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_STATIC_SOURCES: list[dict[str, Any]] = [
    # Yes AI gen not dumb enough to write this long shit myself

    {"id": "fred",                      "name": "FRED",                      "category": "Finance & Economics", "subcategory": "Macroeconomic"},
    {"id": "world_bank",                "name": "World Bank",                "category": "Finance & Economics", "subcategory": "Macroeconomic"},
    {"id": "imf",                       "name": "IMF",                       "category": "Finance & Economics", "subcategory": "Macroeconomic"},
    {"id": "ecb",                       "name": "ECB",                       "category": "Finance & Economics", "subcategory": "Macroeconomic"},
    {"id": "us_treasury",               "name": "US Treasury Fiscal Data",   "category": "Finance & Economics", "subcategory": "Macroeconomic"},
    {"id": "alpha_vantage",             "name": "Alpha Vantage",             "category": "Finance & Economics", "subcategory": "Markets"},
    {"id": "fmp",                       "name": "Financial Modeling Prep",   "category": "Finance & Economics", "subcategory": "Markets"},
    {"id": "coingecko",                 "name": "CoinGecko",                 "category": "Finance & Economics", "subcategory": "Markets"},
    {"id": "exchange_rate",             "name": "ExchangeRate.host",         "category": "Finance & Economics", "subcategory": "Markets"},
    {"id": "stooq",                     "name": "Stooq",                     "category": "Finance & Economics", "subcategory": "Markets"},
    {"id": "sec_edgar",                 "name": "SEC EDGAR",                 "category": "Finance & Economics", "subcategory": "Corporate Intelligence"},
    {"id": "open_corporates",           "name": "OpenCorporates",            "category": "Finance & Economics", "subcategory": "Corporate Intelligence"},
    {"id": "open_ownership",            "name": "Open Ownership",            "category": "Finance & Economics", "subcategory": "Corporate Intelligence"},
    {"id": "companies_house",           "name": "Companies House",           "category": "Finance & Economics", "subcategory": "Corporate Intelligence"},
    {"id": "fpds",                      "name": "Federal Procurement Data System", "category": "Finance & Economics", "subcategory": "Corporate Intelligence"},
    {"id": "ucdp",                      "name": "UCDP",                      "category": "Defense & Geopolitics", "subcategory": "Conflict Databases"},
    {"id": "cow",                       "name": "Correlates of War",         "category": "Defense & Geopolitics", "subcategory": "Conflict Databases"},
    {"id": "icews",                     "name": "ICEWS",                     "category": "Defense & Geopolitics", "subcategory": "Conflict Databases"},
    {"id": "gdelt",                     "name": "GDELT",                     "category": "Defense & Geopolitics", "subcategory": "Conflict Databases"},
    {"id": "phoenix",                   "name": "Phoenix Event Data",        "category": "Defense & Geopolitics", "subcategory": "Conflict Databases"},
    {"id": "sipri_arms",                "name": "SIPRI Arms Transfers",      "category": "Defense & Geopolitics", "subcategory": "Military & Defense"},
    {"id": "sipri_military",            "name": "SIPRI Military Expenditure","category": "Defense & Geopolitics", "subcategory": "Military & Defense"},
    {"id": "nato",                      "name": "NATO Open Data",            "category": "Defense & Geopolitics", "subcategory": "Military & Defense"},
    {"id": "wmeat",                     "name": "WMEAT",                     "category": "Defense & Geopolitics", "subcategory": "Military & Defense"},
    {"id": "un_comtrade",               "name": "UN Comtrade",               "category": "Defense & Geopolitics", "subcategory": "Military & Defense"},
    {"id": "firms",                     "name": "NASA FIRMS",                "category": "Defense & Geopolitics", "subcategory": "Geospatial & Sensors"},
    {"id": "noaa",                      "name": "NOAA",                      "category": "Defense & Geopolitics", "subcategory": "Geospatial & Sensors"},
    {"id": "usgs",                      "name": "USGS Earthquake",           "category": "Defense & Geopolitics", "subcategory": "Geospatial & Sensors"},
    {"id": "osm",                       "name": "OpenStreetMap Overpass",    "category": "Defense & Geopolitics", "subcategory": "Geospatial & Sensors"},
    {"id": "copernicus",                "name": "Copernicus / Sentinel",     "category": "Defense & Geopolitics", "subcategory": "Geospatial & Sensors"},
    {"id": "wikidata",                  "name": "Wikidata",                  "category": "Intelligence & OSINT", "subcategory": "Entity Intelligence"},
    {"id": "dbpedia",                   "name": "DBpedia",                   "category": "Intelligence & OSINT", "subcategory": "Entity Intelligence"},
    {"id": "opensanctions",             "name": "OpenSanctions",             "category": "Intelligence & OSINT", "subcategory": "Entity Intelligence"},
    {"id": "littlesis",                 "name": "LittleSis",                 "category": "Intelligence & OSINT", "subcategory": "Entity Intelligence"},
    {"id": "otx",                       "name": "AlienVault OTX",            "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "virustotal",                "name": "VirusTotal",                "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "abuseipdb",                 "name": "AbuseIPDB",                 "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "urlhaus",                   "name": "URLHaus",                   "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "malwarebazaar",             "name": "MalwareBazaar",             "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "threatfox",                 "name": "ThreatFox",                 "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "circl",                     "name": "CIRCL CVE Search",          "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "nvd",                       "name": "NVD",                       "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "shodan",                    "name": "Shodan InternetDB",         "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "greynoise",                 "name": "GreyNoise",                 "category": "Intelligence & OSINT", "subcategory": "Cyber Threat Intelligence"},
    {"id": "opensky",                   "name": "OpenSky Network",           "category": "Intelligence & OSINT", "subcategory": "Transportation Intelligence"},
    {"id": "adsb_exchange",             "name": "ADS-B Exchange",            "category": "Intelligence & OSINT", "subcategory": "Transportation Intelligence"},
    {"id": "marinetraffic",             "name": "MarineTraffic",             "category": "Intelligence & OSINT", "subcategory": "Transportation Intelligence"},
    {"id": "aishub",                    "name": "AISHub",                    "category": "Intelligence & OSINT", "subcategory": "Transportation Intelligence"},
    {"id": "ourairports",               "name": "OurAirports",               "category": "Intelligence & OSINT", "subcategory": "Transportation Intelligence"},
]

_STATIC_LOOKUP: dict[str, dict[str, Any]] = {s["id"]: s for s in _STATIC_SOURCES}


def _discover_connectors() -> list[dict[str, Any]]:
    from hermes.connectors.base.base_model import Connector

    discovered: list[dict[str, Any]] = []
    connectors_path = Path(__file__).parent / "connectors"

    if not connectors_path.is_dir():
        return discovered

    def _walk_for_connectors(path: Path, package_prefix: str) -> None:
        for entry in path.iterdir():
            if not entry.is_dir() or entry.name.startswith(("_", ".")):
                continue
            init_file = entry / "__init__.py"
            if init_file.exists():
                module_name = f"{package_prefix}.{entry.name}"
                try:
                    mod = importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(mod, inspect.isclass):
                        if (
                            name != "Connector"
                            and issubclass(obj, Connector)
                            and not inspect.isabstract(obj)
                        ):
                            meta = obj.metadata()
                    meta["_connector_class"] = obj
                    discovered.append(meta)
                except Exception:
                    logger.debug("Could not discover connectors from %s", module_name)
            _walk_for_connectors(entry, f"{package_prefix}.{entry.name}")

    _walk_for_connectors(connectors_path, "hermes.connectors")
    return discovered


class SourceRegistry:
    def __init__(self) -> None:
        self._sources: dict[str, dict[str, Any]] = {}

    def discover(self) -> None:
        self._sources = dict(_STATIC_LOOKUP)
        for src in _discover_connectors():
            self._sources[src["id"]] = src

    def is_implemented(self, source_id: str) -> bool:
        src = self._sources.get(source_id)
        if not src:
            return False
        return bool(src.get("credentials") or src.get("parameters") or src.get("outputs"))

    @property
    def source_ids(self) -> list[str]:
        return list(self._sources.keys())

    def get(self, source_id: str) -> dict[str, Any] | None:
        return self._sources.get(source_id)

    @property
    def categories(self) -> list[str]:
        cats: set[str] = set()
        for src in self._sources.values():
            if src.get("category"):
                cats.add(src["category"])
        return sorted(cats)

    def get_by_category(self, category: str) -> list[dict[str, Any]]:
        return sorted(
            [s for s in self._sources.values() if s.get("category") == category],
            key=lambda s: (s.get("subcategory", ""), s["name"]),
        )

    def get_by_category_that_need_credentials(self, category: str) -> list[dict[str, Any]]:
        """Return sources that have credential requirements defined."""
        return sorted(
            [s for s in self._sources.values() if s.get("category") == category and s.get("credentials")],
            key=lambda s: (s.get("subcategory", ""), s["name"]),
        )

    def search(self, query: str) -> list[dict[str, Any]]:
        q = query.lower().strip()
        if not q:
            return sorted(self._sources.values(), key=lambda s: s["name"])
        results = []
        for src in self._sources.values():
            if (
                q in src["id"].lower()
                or q in src["name"].lower()
                or q in src.get("description", "").lower()
                or q in src.get("category", "").lower()
            ):
                results.append(src)
        return sorted(results, key=lambda s: s["name"])
