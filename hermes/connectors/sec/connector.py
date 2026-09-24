import logging
from datetime import timedelta
from functools import partial
from pathlib import Path

import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.connectors.base import BaseConnector
from hermes.core.errors import AcquisitionError
from hermes.credentials.manager import get_cred

logger = logging.getLogger(__name__)

SEC_MAP_PATH = Path(__file__).resolve().parent.parent / "lib" / "datasets" / "cik.parquet"


def sec_mapping(symbol: str) -> str:
    df = pl.scan_parquet(SEC_MAP_PATH).filter(pl.col("ticker") == symbol).collect()
    return df["cik_str"].item()


class SECEDGAR(BaseConnector):
    def __init__(self, cache: RawCache | None = None):
        super().__init__(cache)
        self._email = get_cred("sec_email")
        self._username = get_cred("sec_username")
        self._url = "https://data.sec.gov/api/xbrl/companyfacts"

    def _fetch(self, symbol: str, retries: int = 3, timeout: float = 30.0):
        try:
            cik = sec_mapping(symbol)
        except ValueError:
            logger.warning("unknown ticker: %s", symbol)
            return None
        url = f"{self._url}/{cik}.json"

        headers = {"User-Agent": f"{self._username} {self._email}"}

        try:
            return self._get_json(url, headers=headers, timeout=timeout, retries=retries)
        except AcquisitionError as e:
            if self._not_found(e):
                logger.warning("404: cik=%s", cik)
                return None
            logger.error("HTTP error: %s", e)
            raise

    def fetch(
        self,
        symbol: str,
        timeout: float = 30.0,
        retries: int = 3,
        force: bool = False,
    ) -> pl.DataFrame | dict:
        cache_params = {
            "company": symbol,
        }

        payload = self._cache.get_or_fetch(
            source="sec_edgar",
            params=cache_params,
            fetch_fn=partial(
                self._fetch,
                symbol=symbol,
                timeout=timeout,
                retries=retries,
            ),
            force=force,
            ttl=timedelta(days=7),
        )
        if payload is None:
            return payload
        return self._dataset(payload, f"sec_edgar:{symbol}", source="sec_edgar", params=cache_params)
