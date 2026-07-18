from __future__ import annotations

from pathlib import Path
from typing import Any

from hermes._cache import DataCache
from hermes.sources.bis import BIS
from hermes.sources.comtrade import Comtrade
from hermes.sources.fred import Fred
from hermes.sources.gdelt import GDELT
from hermes.sources.imf import IMF
from hermes.sources.newsapi import NewsAPI
from hermes.sources.ucdp import UCDP
from hermes.sources.v_dem import VDem
from hermes.sources.world_bank import World_Bank


class Hermes:

    def __init__(
        self,
        api_keys: dict[str, str] | None = None,
        cache_dir: str | Path | None = None,
    ):
        api_keys = api_keys or {}
        self._cache = DataCache(cache_dir=cache_dir)

        self.fred = Fred(api_key=api_keys.get("fred"))
        self.world_bank = World_Bank(api_key=api_keys.get("world_bank"))
        self.bis = BIS(api_key=api_keys.get("bis"))
        self.imf = IMF(api_key=api_keys.get("imf"))
        self.gdelt = GDELT(api_key=api_keys.get("gdelt"))
        self.ucdp = UCDP(api_key=api_keys.get("ucdp"))
        self.newsapi = NewsAPI(api_key=api_keys.get("newsapi"))
        self.v_dem = VDem(api_key=api_keys.get("v_dem"))
        self.comtrade = Comtrade(api_key=api_keys.get("comtrade"))

        self.connectors: dict[str, Any] = {
            "fred": self.fred,
            "world_bank": self.world_bank,
            "bis": self.bis,
            "imf": self.imf,
            "gdelt": self.gdelt,
            "ucdp": self.ucdp,
            "newsapi": self.newsapi,
            "v_dem": self.v_dem,
            "comtrade": self.comtrade,
        }

    def list_connectors(self) -> list[dict[str, str]]:
        return [
            {"name": name, "type": type(c).__name__}
            for name, c in self.connectors.items()
        ]

    def get_country_risk_features(
        self,
        country: str,
        date: str | None = None,
        features: list[str] | None = None,
    ) -> dict[str, Any]:
        from hermes.features._risk import get_country_risk_features as _risk
        return _risk(
            country=country,
            date=date,
            connectors=self.connectors,
            cache=self._cache,
            features=features,
        )

    def get_timeseries(
        self,
        country: str,
        indicator: str,
        start: str = "",
        end: str = "",
    ) -> list[dict]:
        from hermes.features._timeseries import get_timeseries as _ts
        return _ts(self.connectors, country, indicator, start, end)
