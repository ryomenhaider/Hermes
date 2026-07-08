import logging

from hermes.config import FRED_API

logger = logging.getLogger(__name__)


class FredAuthenticator:

    
    def authenticate(self) -> bool:
        if not FRED_API:
            logger.error("FRED_API is not set in environment")
            return False
        return True
