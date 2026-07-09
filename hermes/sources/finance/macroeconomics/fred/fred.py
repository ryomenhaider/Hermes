import httpx
from typing import Literal
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class FredLogic:

    def __init__(self, api: str):
        if api:
            self._api = api
        else:
            raise ValueError('The Api is not given')
        
    def fetch_obs(self, series_id: str) -> list[dict]:

        _url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={self._api}&file_type=json'
        
        resp = httpx.get(_url)
        resp.raise_for_status()

        resp = httpx.get(_url)
        
        dat = resp.json()
        
        data = dat['observations']
        
        return data
    
    def fetch_metadata(self, series_id: str) -> dict:
        
        _url = f'https://api.stlouisfed.org/fred/series?series_id={series_id}&api_key={self._api}&file_type=json'

        resp = httpx.get(_url)

        resp.raise_for_status()

        data = resp.content
        data = data.decode()

        return data

    def validate(self, data, type: str = Literal['metadata', 'obs']) -> bool:

        if type == 'metadata':
            
            try:
                if 'seriess' not in data:
                    logger.warning('The Data is not MetaData')
                    return False
                
                elif 'seriess' in data:
                    logger.info('✔ Data is MetaData')
                    logger.info('Conducting futher Inspection')
                    series = data['seriess']
                    
                    checks = ["id", "title", "frequency", "notes", "unit"]
                    
                    in_y = 0
                    in_n = 0

                    for i in checks:
                        if i in series:
                            logger.info(f'✔ {i} is in data')
                            in_y += 1
                            continue

                        elif i not in series:
                            logger.warning(f'✔ {i} not in data')
                            in_n += 1
                            continue
                    
                    if in_n < 1:
                        logger.error('Data is incomplete')
                        return False
                    elif in_n == 0:
                        logger.info('✔ Data is complete')
                        return True

            except Exception as e:
                logger.error(f'Error: {e}')    


        if type == 'obs':
            
            try:

                if 'observations' not in data:
                    logger.error('The data are not observations')
                    return False
                
                elif 'observations' in data:
                    logger.info(f'✔ The data are observation \n there are {data['count']} observations \n doing futher inspections')
                    observations = data['observations']
                    m = 0
                    for index, obs in enumerate(observations):
                        if 'date' not in obs:
                            logger.warning(f'At {index}, the date is missing')
                            continue

                        elif 'value' not in obs:
                            logger.warning(f'At {index}, the value is missing')
                            continue

                        elif obs['value'] == '.':
                            logger.warning(f'The value at {index} of value is "."')
                            m += 1
                            continue       

            except Exception as e:
                logger.error(f'Error: {e}')