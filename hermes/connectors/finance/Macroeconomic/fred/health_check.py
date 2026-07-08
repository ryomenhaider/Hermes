import logging

import httpx

logger = logging.getLogger(__name__)


class FredHealthCheck:

    def health_check(self) -> bool:
        try:
            response = httpx.get(
                "https://api.stlouisfed.org/fred/series"
                "?series_id=GDP"
                "&api_key=test"
                "&file_type=json",
                timeout=5.0,
            )
            return response.status_code != 429
        except httpx.ConnectError:
            logger.error("FRED API is unreachable")
            return False
        except Exception as exc:
            logger.error("Health check failed: %s", exc)
            return False
