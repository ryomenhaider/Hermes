from __future__ import annotations

import logging
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from typing import Any

import polars as pl

from hermes.acquisition.cache import RawCache
from hermes.acquisition.client import Client
from hermes.core.dataset import Dataset, frame_checksum
from hermes.core.errors import AcquisitionError
from hermes.core.provenance import Provenance
from hermes.normalization import NormalizationEngine
from hermes.normalization.rule import NormalizationRule
from hermes.validation import validate
from hermes.validation.rule import ValidationRule

logger = logging.getLogger(__name__)


class BaseConnector:
    #: canonical registry schema this connector's canonical output conforms to
    canonical_schema: str = ""
    def __init__(
        self,
        cache: RawCache | None = None,
        *,
        retry_auth: bool = False,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._cache = cache or RawCache()
        self._retry_auth = retry_auth
        self._headers = dict(headers or {})

    def _get_json(
        self,
        url: str,
        *,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        timeout: float = 30.0,
        retries: int = 3,
    ) -> Any:
        merged = {**self._headers, **(headers or {})}
        with Client(timeout=timeout, max_retries=retries, retry_auth=self._retry_auth) as client:
            return client.get(url, params=params, headers=merged)

    @staticmethod
    def _not_found(error: Exception) -> bool:
        return isinstance(error, AcquisitionError) and getattr(error, "status_code", None) == 404

    def _normalize(self, data: pl.DataFrame, rules: list[NormalizationRule]) -> pl.DataFrame:
        if not rules:
            return data
        return NormalizationEngine(rules).normalize(data)

    def _validate(self, data: pl.DataFrame, rules: list[ValidationRule], source: str) -> None:
        if not rules or data.is_empty():
            return
        result = validate(data, rules)
        if not result.passed:
            logger.warning("%s validation failed:\n%s", source, result.summary())

    def _dataset(self, payload: Any, name: str, *, source: str, params: dict | None = None) -> Dataset:
        dataset = Dataset(
            name=name,
            data=payload,
            provenance=Provenance(
                source=source,
                connector=type(self).__name__.lower(),
                connector_version=self._hermes_version(),
                retrieved_at=datetime.now(tz=UTC),
                raw_checksum=frame_checksum(payload),
            ),
        )
        dataset.record("fetch", input_ref=source, params=params or {})
        return dataset

    @staticmethod
    def _hermes_version() -> str | None:
        try:
            return version("hermes-plt")
        except PackageNotFoundError:
            return None


__all__ = ["BaseConnector"]
