import logging
from datetime import timedelta
from functools import partial

import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.base import BaseConnector
from hermes.connectors.world_bank.mappings import WORLD_BANK_BASE_URL
from hermes.connectors.world_bank.parser import records_to_dataframe
from hermes.core.dataset import Dataset
from hermes.core.errors import AcquisitionError
from hermes.normalization import NormalizeCountry, NormalizeDate
from hermes.validation import NotNull

logger = logging.getLogger(__name__)

_EMPTY_SCHEMA = {
    "date": pl.String,
    "indicator_id": pl.String,
    "indicator_name": pl.String,
    "country": pl.String,
    "value": pl.String,
    "source": pl.String,
}


class World_bank(BaseConnector):
    canonical_schema = "economic.observation"

    def __init__(self, cache: RawCache | None = None):
        super().__init__(cache)
        self.url = WORLD_BANK_BASE_URL

    def _fetch(
        self,
        country_code: str,
        indicator_code: str,
        frequency: str | None = None,
        most_recent: int | None = None,
        per_page: int = 1000,
        page: int = 1,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> pl.DataFrame:
        url = f"{self.url}/country/{country_code}/indicator/{indicator_code}"
        params = {
            "per_page": per_page,
            "page": page,
            "format": "json",
        }
        if frequency and most_recent:
            params["frequency"] = frequency
            params["mrv"] = most_recent

        try:
            r = self._get_json(url, params=params, timeout=timeout, retries=retries)
        except AcquisitionError as e:
            logger.error("HTTP error: %s", e)
            raise

        if len(r) < 2 or not r[1]:
            logger.info(f"No data: country={country_code}, indicator={indicator_code}")
            return pl.DataFrame(schema=_EMPTY_SCHEMA)

        _, records = r[0], r[1]

        return records_to_dataframe(records)

    def fetch(
        self,
        country_code: str,
        indicator_code: str,
        frequency: str | None = None,
        most_recent: int | None = None,
        per_page: int = 1000,
        page: int = 1,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> Dataset:
        cache_params = {
            "country": country_code,
            "indicator": indicator_code,
            "frequency": frequency or "",
            "most_recent": most_recent or 0,
            "per_page": per_page,
        }

        df = self._cache.get_or_fetch(
            source="world_bank",
            params=cache_params,
            fetch_fn=partial(
                self._fetch,
                country_code,
                indicator_code,
                frequency,
                most_recent,
                per_page,
                page,
                timeout,
                retries,
            ),
            force=force,
            ttl=timedelta(days=7),  # WB data updates weekly
        )
        df = self._normalize(df, [NormalizeDate("date"), NormalizeCountry("country")])
        self._validate(df, [NotNull("date"), NotNull("country"), NotNull("value")], "world_bank")
        return self._dataset(
            df,
            f"world_bank:{country_code}:{indicator_code}",
            source="world_bank",
            params=cache_params,
        )
