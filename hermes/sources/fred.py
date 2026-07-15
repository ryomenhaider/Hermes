import httpx
from typing import Literal
import pandas as pd
import logging
import time
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

FRED_API = os.getenv('FRED_API')

class FredLogic:
        
    def fetch_obs(self, series_id: str, _api: str) -> tuple[dict, list]:

        _url = f'https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={_api}&file_type=json'

        resp = httpx.get(_url)
        resp.raise_for_status()

        data = resp.content
        data = data.decode()

        return data
    
    def fetch_metadata(self, series_id: str, _api: str) -> dict:

        _url = f'https://api.stlouisfed.org/fred/series?series_id={series_id}&api_key={_api}&file_type=json'

        resp = httpx.get(_url)
        resp.raise_for_status()

        data = resp.content
        data = data.decode()
        
        series = data['seriess'][0]
        return series

    def validate(self, data, type: Literal['metadata', 'obs']) -> bool:

        if type == 'metadata':
            try:
                if not isinstance(data, dict) or 'seriess' not in data:
                    logger.warning('The Data is not MetaData')
                    return False

                logger.info('✔ Data is MetaData')
                logger.info('Conducting further inspection')
                series = data['seriess'][0]

                checks = ["id", "title", "frequency", "notes", "units"]
                missing = [field for field in checks if field not in series]

                for field in checks:
                    if field in series:
                        logger.info(f'✔ {field} is in data')
                    else:
                        logger.warning(f'✖ {field} not in data')

                if missing:
                    logger.error('Data is incomplete')
                    return False

                logger.info('✔ Data is complete')
                return True

            except Exception as e:
                logger.error(f'Error: {e}')
                return False

        elif type == 'obs':
            try:
                if 'observations' not in data:
                    logger.error('The data are not observations')
                    return False

                logger.info('✔ The data are observations, doing further inspections')
                observations = data['observations']
                issues = 0

                for index, obs in enumerate(observations):
                    if 'date' not in obs:
                        logger.warning(f'At {index}, the date is missing')
                        issues += 1
                        continue

                    if 'value' not in obs:
                        logger.warning(f'At {index}, the value is missing')
                        issues += 1
                        continue

                    if obs.get('value') == '.':
                        logger.warning(f'The value at {index} is "."')
                        continue

                if issues > 0:
                    logger.error(f'Observations contain missing or placeholder values, Total Issues: {issues}')
                    return True

                return True

            except Exception as e:
                logger.error(f'Error: {e}')
                return False

        else:
            logger.error(f"The type should only be 'metadata' or 'obs', you gave {type!r}")
            return False

    def transform(self, data, type: Literal['metadata', 'obs']) -> pd.DataFrame:

        if type == 'metadata':

            series = data['seriess'] if 'seriess' in data else [data]
            df = pd.DataFrame(series).set_index('id')

            date_cols = ['realtime_start', 'realtime_end', 'observation_start', 'observation_end']
            for col in date_cols:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col])

            if 'popularity' in df.columns:
                df['popularity'] = pd.to_numeric(df['popularity'], errors='coerce')

            return df
        
        if type == 'obs':
            
            return (
                pd.DataFrame(data['observations'])
                .assign(
                    date           = lambda x: pd.to_datetime(x['date']),
                    value          = lambda x: pd.to_numeric(x['value'], errors='coerce'),
                    realtime_start = lambda x: pd.to_datetime(x['realtime_start']),
                    realtime_end   = lambda x: pd.to_datetime(x['realtime_end'])
                )
                .set_index('date')
                .sort_index()
            )
        
        raise ValueError(f"Invalid type: {type!r}. Must be 'metadata' or 'obs'.")
    
    def export(self, data: pd.DataFrame, filetype: str) -> str:

        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        ts = time.time()
        path = f'data/{ts}.{filetype}'

        if filetype == 'json':
            data.reset_index().to_json(path, orient='records', date_format='iso')

        elif filetype == 'csv':
            data.to_csv(path, date_format='iso')

        elif filetype == 'parquet':
            data.to_parquet(path)

        elif filetype == 'pickle':
            data.to_pickle(path)

        else:
            raise ValueError(f"Unsupported filetype: {filetype!r}")

        logger.info(f'Exported to {path}')
        return path
    

class Fred:

    def __init__(self):
        self.fred_logic = FredLogic()

    def fred_api(self, api: str):
        return api
    
    def get_series(self, series_id : str, api: str):
        if not api:
            raise ValueError(
                """
                    You must provide an Fred API
                    You can obtain it by getting the API from the official FRED website
                    And then you can call the hermes inbuild function fred_api() function to just set it up
                    like this
                            api = fred.fred_api('XXXXXXXXXXXXXX')
                    and then after you can use it like this
                            data = get_series('GDP', api)
                                
                    NOTE: The data return is transformed and in pd.DataFrame
                """
            )
        print('============ FETCHING OBSERVATION ============')
        data = self.fred_logic.fetch_obs(series_id=series_id, _api=api)

        print('=========== VALIDATING OBSERVATION ===========')
        vl = self.fred_logic.validate(data, type='obs')

        print('========== TRANSFORMING OBSERVATION ==========')
        if vl == True:
            transformed_data = self.fred_logic.transform(data, type='obs')
            return transformed_data
        
        else:
            raise RuntimeError('The Data is not valid for application')

