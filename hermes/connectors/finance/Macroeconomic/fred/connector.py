from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

import httpx
import pandas as pd

from hermes.connectors.base.base_model import Connector
from hermes.credentials import get_credential
from hermes.config import FRED_API

logger = logging.getLogger(__name__)

BASE_URL = "https://api.stlouisfed.org/fred"


class FredConnector(Connector):

    @classmethod
    def metadata(cls) -> dict:
        return {
            "id": "fred",
            "name": "FRED",
            "category": "Finance & Economics",
            "subcategory": "Macroeconomic",
            "description": "Federal Reserve Economic Data (FRED) — thousands of US and international economic time series from the Federal Reserve Bank of St. Louis.",
            "credentials": [
                {"key": "api_key", "label": "API Key"},
            ],
            "parameters": [
                {"name": "series_id", "type": "string", "label": "Series ID", "default": "CPIAUCSL"},
                {"name": "start_date", "type": "string", "label": "Start Date", "default": "2020-01-01"},
                {"name": "end_date", "type": "string", "label": "End Date", "default": ""},
                {"name": "limit", "type": "integer", "label": "Max Records", "default": 100000},
            ],
            "outputs": ["CSV", "JSON", "Parquet"],
        }

    def _get_api_key(self) -> str:
        stored = get_credential("fred", {})
        key = stored.get("api_key", "")
        if key:
            return key
        if FRED_API:
            return FRED_API
        raise ValueError("FRED API key not found. Set FRED_API env var or save via Credentials screen.")

    def authenticate(self) -> bool:
        try:
            self._get_api_key()
            return True
        except ValueError:
            return False

    def validate_credentials(self) -> bool:
        try:
            key = self._get_api_key()
            resp = httpx.get(
                f"{BASE_URL}/series/observations",
                params={"series_id": "CPIAUCSL", "api_key": key, "limit": 1, "file_type": "json"},
                timeout=10,
            )
            return resp.status_code == 200 and resp.json().get("error_code") is None
        except Exception:
            return False

    def fetch(self, **kwargs) -> list[dict[str, Any]]:
        series_id = kwargs.get("series_id", "CPIAUCSL")
        limit = kwargs.get("limit", 100000)
        start_date = kwargs.get("start_date", "2020-01-01")
        end_date = kwargs.get("end_date", "")

        key = self._get_api_key()
        params: dict[str, Any] = {
            "series_id": series_id,
            "api_key": key,
            "file_type": "json",
            "limit": limit,
            "sort_order": "asc",
            "observation_start": start_date,
        }
        if end_date:
            params["observation_end"] = end_date

        logger.info("Fetching FRED series %s", series_id)
        resp = httpx.get(f"{BASE_URL}/series/observations", params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if "error_code" in data:
            raise RuntimeError(f"FRED API error {data['error_code']}: {data.get('error_message', '')}")

        observations = data.get("observations", [])
        results = []
        for obs in observations:
            val = obs.get("value")
            if val and val != ".":
                results.append({
                    "series_id": series_id,
                    "date": obs.get("date"),
                    "value": float(val) if val.replace(".", "", 1).isdigit() else None,
                })
        return results

    def validate(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        validated = []
        for row in data:
            if row.get("date") and row.get("value") is not None:
                validated.append(row)
        return validated

    def transform(self, data: list[dict[str, Any]]) -> pd.DataFrame:
        return pd.DataFrame(data)

    def export(self, data: list[dict[str, Any]], destination: str) -> None:
        df = pd.DataFrame(data)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        if destination == "CSV":
            df.to_csv(f"fred_export_{ts}.csv", index=False)
        elif destination == "JSON":
            df.to_json(f"fred_export_{ts}.json", orient="records", indent=2)
        elif destination == "Parquet":
            df.to_parquet(f"fred_export_{ts}.parquet", index=False)
        else:
            logger.warning("Unsupported destination: %s", destination)

    def health_check(self) -> dict:
        try:
            t0 = datetime.now()
            key = self._get_api_key()
            resp = httpx.get(
                f"{BASE_URL}/series/observations",
                params={"series_id": "CPIAUCSL", "api_key": key, "limit": 1, "file_type": "json"},
                timeout=10,
            )
            elapsed = (datetime.now() - t0).total_seconds()
            return {
                "status": "ok" if resp.status_code == 200 else "error",
                "latency": f"{elapsed:.2f}s",
                "status_code": resp.status_code,
            }
        except Exception as exc:
            return {"status": "error", "error": str(exc)}
