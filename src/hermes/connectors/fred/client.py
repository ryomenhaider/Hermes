import httpx
from config import FRED_API
import logging
from indicators import FRED_INDICATORS
from typing import Literal

logger = logging(__name__)
class FredClient:

    def __init__(self):
        self._api = FRED_API

    def get_url(self,
            series_id: str, 
            endpoint: str = 'MetaData' | 'Observations'
            ) -> str:

        VALID_SERIES_IDS = {
            item["series_id"]
            for item in FRED_INDICATORS
        }

        if series_id in VALID_SERIES_IDS:

            if endpoint == 'MetaData':
                return f'https://api.stlouisfed.org/fred/series?series_id={series_id}&api_key={self._api}&file_type=json' 
            elif endpoint == 'Observations':
                return f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={self._api}&file_type=json'
            else:
                logger.error(f'Wront EndPoint')

        else:
            logger.error(f'{series_id} is not available')


    def get_data(self, endpoint: Literal['metadata', 'observations']):

        results = []

        for item in FRED_INDICATORS:
            try:
                series_id = item['series_id']
                url = self.get_url(
                    series_id=series_id, 
                    endpoint=endpoint
                )
                
                response = httpx.get(url)
                response.raise_for_status()
                
                results.append(
                    {
                        'series_id': series_id,
                        'data': response.json()
                    }
                )
            
            except Exception as e:
                logger.error(f'Error: {e}')    

        return results