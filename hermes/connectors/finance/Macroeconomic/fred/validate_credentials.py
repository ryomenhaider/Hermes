import logging

import httpx

from hermes.config import FRED_API

logger = logging.getLogger(__name__)


class FredCredentialValidator:

    def validate_credentials(self) -> bool:
        test_url = (
            "https://api.stlouisfed.org/fred/series"
            f"?series_id=GDP"
            f"&api_key={FRED_API}"
            f"&file_type=json"
        )
        try:
            response = httpx.get(test_url, timeout=10.0)
            response.raise_for_status()
            return True
        except Exception as exc:
            logger.error("Credential validation failed: %s", exc)
            return False
