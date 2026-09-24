import logging
from datetime import timedelta
from functools import partial

import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.base import BaseConnector
from hermes.connectors.imf.mappings import IMF_BASE_URL
from hermes.connectors.imf.parser import empty_dataframe, parse_sdmx_json
from hermes.core.dataset import Dataset
from hermes.core.errors import AcquisitionError
from hermes.normalization import NormalizeCountry, NormalizeDate
from hermes.validation import NotNull

logger = logging.getLogger(__name__)


class IMF(BaseConnector):
    canonical_schema = "economic.observation"

    def __init__(self, cache: RawCache | None = None):
        super().__init__(cache)
        self.url: str = IMF_BASE_URL

    def _fetch(
        self,
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        version: str = "~",
        timeout: float = 30.0,
        retries: int = 3,
    ) -> pl.DataFrame:
        url = f"{self.url}{agency}/{dataflow_id}/{version}/{country}.{key}"
        headers = {"Accept": "application/json"}

        empty = empty_dataframe()

        try:
            r = self._get_json(url, headers=headers, timeout=timeout, retries=retries)
        except AcquisitionError as e:
            if self._not_found(e):
                logger.warning(f"404: country={country}, dataflow={dataflow_id}, key={key}")
                return empty
            logger.error("HTTP error: %s", e)
            raise
        return parse_sdmx_json(r["data"], country=country, key=key)

    def fetch(
        self,
        country: str,
        agency: str,
        dataflow_id: str,
        key: str,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> Dataset:
        cache_params = {
            "country": country,
            "key": key,
            "agency": agency,
            "dataflow_id": dataflow_id,
        }

        df = self._cache.get_or_fetch(
            source="imf",
            params=cache_params,
            fetch_fn=partial(
                self._fetch,
                country=country,
                agency=agency,
                dataflow_id=dataflow_id,
                key=key,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )
        df = self._normalize(df, [NormalizeDate("date"), NormalizeCountry("country")])
        self._validate(df, [NotNull("country"), NotNull("value")], "imf")
        return self._dataset(
            df,
            f"imf:{agency}:{dataflow_id}:{key}",
            source="imf",
            params=cache_params,
        )
