import logging
from datetime import timedelta
from functools import partial

from hermes.acquisition.cache import RawCache
from hermes.connectors.base import BaseConnector
from hermes.core.errors import AcquisitionError
from hermes.credentials.manager import get_cred
from hermes.entities.countries import iso3_to_iso2

logger = logging.getLogger(__name__)


class OpenSanction(BaseConnector):
    canonical_schema = "entity"

    def __init__(self, cache: RawCache | None = None):
        self._base_url = "https://api.opensanctions.org"
        self._api_key = get_cred("opensanction")
        self._headers = {"Authorization": f"ApiKey {self._api_key}", "Accept": "application/json"}
        super().__init__(cache, headers=self._headers)

    def _fetch(
        self,
        country: str,
        dataset: str,
        limit: int = 50,
        changed_since: str = None,
        topics: str = None,
        facets: str = None,
        retries: int = 3,
        timeout: float = 30.0,
    ) -> dict:
        """
        Fetch raw sanctions data from OpenSanctions API.
        Returns raw JSON response as dict.

        Common datasets:
        - us_ofac_sdn: US OFAC Specially Designated Nationals
        - eu_fsf: EU Financial Sanctions Files
        - uk_fcdos: UK FCDO Sanctions List
        - un_sc: UN Security Council Sanctions
        """
        if not dataset:
            raise ValueError("dataset parameter is empty")

        country_iso2 = iso3_to_iso2(country)
        if not country_iso2:
            logger.warning(f"Invalid country code: {country}")
            return {}

        url = f"{self._base_url}/search/{dataset}"

        params = {"countries": country_iso2, "limit": min(limit, 500)}

        if changed_since:
            params["changed_since"] = changed_since
        if topics:
            params["topics"] = topics
        if facets:
            params["facets"] = facets

        logger.info(f"Fetching from: {url}")
        logger.info(f"Params: {params}")

        try:
            return self._get_json(url, params=params, timeout=timeout, retries=retries)
        except AcquisitionError as e:
            if self._not_found(e):
                logger.error(f"Dataset '{dataset}' not found")
                return {}
            logger.error("HTTP error: %s", e)
            raise

    def fetch(
        self,
        country: str,
        dataset: str,
        limit: int = 50,
        changed_since: str | None = None,
        topic: str | None = None,
        facets: str | None = None,
        retries: int = 3,
        timeout: float = 30.0,
        force: bool = False,
    ):
        cached_params = {
            "country": country,
            "dataset": dataset,
        }

        payload = self._cache.get_or_fetch(
            source="OpenSanction",
            params=cached_params,
            fetch_fn=partial(
                self._fetch,
                country=country,
                dataset=dataset,
                limit=limit,
                changed_since=changed_since,
                topics=topic,
                facets=facets,
                retries=retries,
                timeout=timeout,
            ),
            force=force,
            ttl=timedelta(days=7),
        )
        if payload is None:
            return payload
        return self._dataset(
            payload,
            f"opensanctions:{country}:{dataset}",
            source="opensanctions",
            params=cached_params,
        )
