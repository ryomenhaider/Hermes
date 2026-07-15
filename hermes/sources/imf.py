import pandas as pd
import httpx
import logging

logger = logging.getLogger(__name__)

base_url = "https://www.imf.org/external/datamapper/api/v1"

class IMFLogic:

    def fetch():
        pass

class IMF:

    def get_dataset(self):
        
        r = httpx.get(base_url)
        r.raise_for_status()
        r = r.json()
        