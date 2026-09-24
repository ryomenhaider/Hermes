import logging
from datetime import timedelta
from functools import partial

import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.base import BaseConnector
from hermes.connectors.fred.parser import observations_to_dataframe
from hermes.core.dataset import Dataset
from hermes.core.errors import AcquisitionError
from hermes.credentials.manager import get_cred
from hermes.normalization import NormalizeDate
from hermes.validation import NotNull

logger = logging.getLogger(__name__)


class FRED(BaseConnector):
    canonical_schema = "economic.observation"

    def __init__(self, api: str, cache: RawCache | None = None):
        super().__init__(cache)
        self._url = "https://api.stlouisfed.org/fred/series/observations"
        self._api = get_cred("fred")

    def _fetch(self, series_id: str, timeout: float = 30.0, retries: int = 3) -> pl.DataFrame:
        params = {"series_id": series_id, "api_key": self._api, "file_type": "json"}

        try:
            r = self._get_json(self._url, params=params, timeout=timeout, retries=retries)
        except AcquisitionError as e:
            if self._not_found(e):
                logger.warning("404: series_id=%s", series_id)
                return None
            raise

        return observations_to_dataframe(r, series_id)

    def fetch(self, series_id: str, timeout: float = 30.0, retries: int = 3, force: bool = False) -> Dataset | None:
        cached_params = {"series_id": series_id}

        df = self._cache.get_or_fetch(
            source="fred",
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                series_id=series_id,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=30),
        )
        if df is None:
            return df
        df = self._normalize(df, [NormalizeDate("date")])
        self._validate(df, [NotNull("date"), NotNull("value")], "fred")
        return self._dataset(df, f"fred:{series_id}", source="fred", params=cached_params)
