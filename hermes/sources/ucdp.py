from __future__ import annotations

import pandas as pd
import logging
from typing import Any

from hermes.base import BaseConnector

logger = logging.getLogger(__name__)


class UCDP(BaseConnector):
    """UCDP (Uppsala Conflict Data Program) connector.

    Provides battle-related deaths, organized violence event data,
    and conflict type classifications for geopolitical risk analysis.
    """

    def __init__(self, api_key: str | None = None):
        super().__init__()
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "ucdp"

    def fetch(
        self,
        country: str = "",
        indicator: str = "battle_deaths",
        **kwargs: Any,
    ) -> pd.DataFrame:
        """Fetch UCDP data for a country.

        Parameters
        ----------
        country : str
            ISO3 country code.
        indicator : str
            One of 'battle_deaths', 'ged' (Georeferenced Event Dataset), 'conflict_type'.
        """
        return pd.DataFrame(columns=["date", "country", "indicator", "value", "source"])

    def get_available_countries(self) -> list[str]:
        return ["AFG", "IRQ", "SYR", "UKR", "YEM", "SOM", "SSD", "MMR", "ETH", "COD", "SDN", "COL", "MEX"]

    def get_date_range(self, country: str) -> tuple[str, str]:
        return ("1989-01-01", "")
