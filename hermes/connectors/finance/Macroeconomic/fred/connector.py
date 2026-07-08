from __future__ import annotations

import logging
from typing import Any

from hermes.connectors.base_model import Connector
from hermes.connectors.finance.Macroeconomic.fred.authenticate import FredAuthenticator
from hermes.connectors.finance.Macroeconomic.fred.export import FredExporter
from hermes.connectors.finance.Macroeconomic.fred.fetch import FredClient
from hermes.connectors.finance.Macroeconomic.fred.health_check import FredHealthCheck
from hermes.connectors.finance.Macroeconomic.fred.transform import FredTransformer
from hermes.connectors.finance.Macroeconomic.fred.validate import FredValidator
from hermes.connectors.finance.Macroeconomic.fred.validate_credentials import (
    FredCredentialValidator,
)

logger = logging.getLogger(__name__)


class FredConnector(Connector):
    VALID_ENDPOINTS = {"metadata", "observations"}

    def __init__(
        self,
        series_ids: list[str],
        endpoint: str = "observations",
    ):
        effective_endpoint = endpoint.strip().lower()
        if effective_endpoint not in self.VALID_ENDPOINTS:
            raise ValueError(
                f"Unsupported endpoint: {effective_endpoint}. "
                f"Supported endpoints: {sorted(self.VALID_ENDPOINTS)}"
            )

        self.series_ids = series_ids
        self.endpoint = effective_endpoint

        self._authenticator = FredAuthenticator()
        self._credential_validator = FredCredentialValidator()
        self._client = FredClient()
        self._validator = FredValidator()
        self._transformer = FredTransformer()
        self._exporter = FredExporter()
        self._health_check = FredHealthCheck()

    def authenticate(self) -> bool:
        return self._authenticator.authenticate()

    def validate_credentials(self) -> bool:
        return self._credential_validator.validate_credentials()

    def fetch(self) -> list[dict[str, Any]]:
        raw = self._client.get_data(self.series_ids, self.endpoint)
        if not raw:
            logger.warning("No FRED payload returned for endpoint %s", self.endpoint)
        return raw

    def validate(self) -> list[dict[str, Any]]:
        validated: list[dict[str, Any]] = []

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

            validated.append({"series_id": series_id, "payload": valid_payload})

        return validated

    def transform(self) -> list[dict[str, Any]]:
        return self._transformer.transform(self.validate(), self.endpoint)

    def export(self, data: list[dict[str, Any]], destination: str) -> None:
        self._exporter.export(data, destination)

    def health_check(self) -> bool:
        return self._health_check.health_check()
