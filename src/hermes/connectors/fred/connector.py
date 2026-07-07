from __future__ import annotations

import logging
from typing import Any

from src.hermes.connectors.base_model import Connector
from src.hermes.connectors.fred.client import FredClient
from src.hermes.connectors.fred.mapper import FredMapper
from src.hermes.connectors.fred.repository import FredRepo
from src.hermes.connectors.fred.validator import FredValidator

logger = logging.getLogger(__name__)


class FredConnector(Connector):
    VALID_ENDPOINTS = {"metadata", "observations"}

    def __init__(self, endpoint: str):
        effective_endpoint = endpoint.strip().lower()
        if not effective_endpoint:
            raise ValueError("FredConnector requires an endpoint.")
        if effective_endpoint not in self.VALID_ENDPOINTS:
            raise ValueError(
                f"Unsupported endpoint: {effective_endpoint}. "
                f"Supported endpoints: {sorted(self.VALID_ENDPOINTS)}"
            )

        self.endpoint = effective_endpoint
        self._client = FredClient()
        self._validator = FredValidator()
        self._mapper = FredMapper()
        self._repo = FredRepo()

    def fetch(self) -> list[dict[str, Any]]:
        raw_results = self._client.get_data(self.endpoint)
        if not raw_results:
            logger.warning("No FRED payload returned for endpoint %s", self.endpoint)
        return raw_results

    def validate(self) -> list[dict[str, Any]]:
        validated_results: list[dict[str, Any]] = []

        for result in self.fetch():
            series_id = result.get("series_id")
            payload = result.get("data", {})

            try:
                valid_payload = self._validator.validate(payload, self.endpoint)
            except Exception as exc:
                logger.error(
                    "Validation failed for series %s endpoint %s: %s",
                    series_id,
                    self.endpoint,
                    exc,
                )
                continue

            if not valid_payload:
                logger.info(
                    "No valid payload for series %s endpoint %s",
                    series_id,
                    self.endpoint,
                )
                continue

            validated_results.append({"series_id": series_id, "payload": valid_payload})

        return validated_results

    def mapper(self) -> list[dict[str, Any]]:
        mapped_results: list[dict[str, Any]] = []

        for result in self.validate():
            series_id = result["series_id"]
            payload = result["payload"]

            try:
                if self.endpoint == "metadata":
                    for metadata_item in payload:
                        mapped_results.append(
                            self._mapper.map(metadata_item, self.endpoint)
                        )
                else:
                    observations = self._mapper.map(
                        payload, self.endpoint, series_id=series_id
                    )
                    mapped_results.append(
                        {"series_id": series_id, "observations": observations}
                    )
            except Exception as exc:
                logger.error(
                    "Mapping failed for series %s endpoint %s: %s",
                    series_id,
                    self.endpoint,
                    exc,
                )

        return mapped_results

    def store(self) -> None:
        mapped_items = self.mapper()
        if not mapped_items:
            logger.warning("No mapped items to store for endpoint %s", self.endpoint)
            return

        for item in mapped_items:
            if self.endpoint == "metadata":
                self._repo.upsert_metadata(item)
                logger.info("Metadata stored for %s", item.get("id"))
            else:
                self._repo.upsert_obs(item["series_id"], item["observations"])
                logger.info("Observations stored for %s", item["series_id"])

