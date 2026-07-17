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
FRED_BASE = 'https://api.stlouisfed.org/fred'


class FredLogic:

    def fetch_obs(self, series_id: str, _api: str) -> dict:
        url = f'{FRED_BASE}/series/observations?series_id={series_id}&api_key={_api}&file_type=json'
        resp = httpx.get(url)
        resp.raise_for_status()
        return series_id ,resp.json()

    def fetch_metadata(self, series_id: str, _api: str) -> dict:
        url = f'{FRED_BASE}/series?series_id={series_id}&api_key={_api}&file_type=json'
        resp = httpx.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data['seriess'][0]

    def fetch_search(self, query: str, _api: str, limit: int = 25) -> dict:
        url = f'{FRED_BASE}/series/search?search_text={query}&api_key={_api}&file_type=json&limit={limit}'
        resp = httpx.get(url)
        resp.raise_for_status()
        return resp.json()

    def fetch_categories(self, _api: str) -> dict:
        url = f'{FRED_BASE}/category?api_key={_api}&file_type=json'
        resp = httpx.get(url)
        resp.raise_for_status()
        return resp.json()

    def fetch_series_in_category(self, category_id: int, _api: str, limit: int = 100) -> dict:
        url = f'{FRED_BASE}/category/series?category_id={category_id}&api_key={_api}&file_type=json&limit={limit}'
        resp = httpx.get(url)
        resp.raise_for_status()
        return resp.json()

    def validate(self, data, type: Literal['metadata', 'obs']) -> bool:
        if type == 'metadata':
            try:
                if not isinstance(data, dict) or 'seriess' not in data:
                    logger.warning('The Data is not MetaData')
                    return False

                logger.info('Data is MetaData')
                series = data['seriess'][0]

                checks = ["id", "title", "frequency", "notes", "units"]
                missing = [field for field in checks if field not in series]

                for field in checks:
                    if field in series:
                        logger.info(f'{field} is in data')
                    else:
                        logger.warning(f'{field} not in data')

                if missing:
                    logger.error('Data is incomplete')
                    return False

                logger.info('Data is complete')
                return True

            except Exception as e:
                logger.error(f'Error: {e}')
                return False

        elif type == 'obs':
            try:
                if 'observations' not in data:
                    logger.error('The data are not observations')
                    return False

                logger.info('The data are observations, doing further inspections')
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

    def transform(self, data, series_id: str, type: Literal['metadata', 'obs']) -> pd.DataFrame:
        
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
                    country_iso3   = 'USA',
                    indicator_id   = series_id,
                    value          = lambda x: pd.to_numeric(x['value'], errors='coerce'),
                    source         = 'FRED'
                )
                .set_index('date')
                .sort_index()
            )

        raise ValueError(f"Invalid type: {type!r}. Must be 'metadata' or 'obs'.")

    def transform_search(self, data: dict) -> pd.DataFrame:
        seriess = data.get('seriess', [])
        if not seriess:
            return pd.DataFrame(columns=['id', 'title', 'frequency', 'units', 'popularity'])
        return pd.DataFrame(seriess)
    


    def export(self, data: pd.DataFrame, filetype: str) -> str:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        ts = time.time()
        path = f'data/fred{ts}.{filetype}'

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


COMMON_SERIES = {
    "GDP": "GDP",
    "UNEMPLOYMENT": "UNRATE",
    "CPI": "CPIAUCSL",
    "INFLATION": "FPCPITOTLZGUSA",
    "FED_FUNDS_RATE": "FEDFUNDS",
    "TREASURY_10Y": "DGS10",
    "TREASURY_2Y": "DGS2",
    "SP500": "SP500",
    "VIX": "VIXCLS",
    "INDUSTRIAL_PRODUCTION": "INDPRO",
    "RETAIL_SALES": "RSXFS",
    "HOUSING_STARTS": "HOUST",
    "POPULATION": "POP",
    "DEBT_TO_GDP": "GFDEGDQ188S",
    "PERSONAL_SAVINGS_RATE": "PSAVERT",
    "CONSUMER_SENTIMENT": "UMCSENT",
}


class Fred:

    def __init__(self):
        self.fred_logic = FredLogic()
        self._api = None

    def connect(self, api_key: str) -> str:
        self._api = api_key
        logger.info('FRED API key stored')
        return self._api

    def get_series(
        self,
        series_id: str,
        api: str = None,
        export: bool | None = None,
        filetype: str | None = None,
    ):
        key = api or self._api
        if not key:
            raise ValueError(
                "Provide an API key via .connect('KEY') or pass api='KEY'"
            )
        id, data = self.fred_logic.fetch_obs(series_id=series_id, _api=key)

        vl = self.fred_logic.validate(data, type='obs')

        if vl is True:
            transformed_data = self.fred_logic.transform(data,series_id=id , type='obs')

            if export is True:
                self.fred_logic.export(transformed_data, filetype=filetype)

            return transformed_data

        raise RuntimeError('The Data is not valid for application')

    def _get_metadata(self, series_id: str, key: str) -> dict | None:
        try:
            return self.fred_logic.fetch_metadata(series_id, _api=key)
        except Exception:
            return None

    def get_series_metadata(
        self,
        series_id: str,
        api: str = None,
        export: bool | None = None,
        filetype: str | None = None,
        normalize: bool = True,
    ) -> pd.DataFrame:
        key = api or self._api
        if not key:
            raise ValueError(
                "Provide an API key via .connect('KEY') or pass api='KEY'"
            )
        data = self.fred_logic.fetch_metadata(series_id=series_id, _api=key)
        vl = self.fred_logic.validate(data, type='metadata')

        if vl is True:
            transformed_data = self.fred_logic.transform(data, type='metadata')

            if export is True:
                self.fred_logic.export(transformed_data, filetype=filetype)

            return transformed_data

        raise RuntimeError('The Data is not valid for application')

    def search_series(
        self,
        query: str,
        limit: int = 25,
        api: str = None,
    ) -> pd.DataFrame:
        key = api or self._api
        if not key:
            raise ValueError(
                "Provide an API key via .connect('KEY') or pass api='KEY'"
            )
        data = self.fred_logic.fetch_search(query=query, _api=key, limit=limit)
        return self.fred_logic.transform_search(data)

    def get_multiple_series(
        self,
        series_ids: list[str],
        api: str = None,
        export: bool | None = None,
        filetype: str | None = None,
        normalize: bool = True,
    ) -> pd.DataFrame:
        key = api or self._api
        if not key:
            raise ValueError(
                "Provide an API key via .connect('KEY') or pass api='KEY'"
            )
        frames = {}
        for sid in series_ids:
            raw = self.fred_logic.fetch_obs(series_id=sid, _api=key)
            vl = self.fred_logic.validate(raw, type='obs')
            if vl is True:
                df = self.fred_logic.transform(raw, type='obs')
                frames[sid] = df[['date', 'value']].set_index('date')['value'] if normalize else df['value']

        result = pd.concat(frames, axis=1)
        result.columns.name = 'series_id'

        if export is True:
            self.fred_logic.export(result, filetype=filetype)

        return result

    def get_categories(self, api: str = None) -> pd.DataFrame:
        key = api or self._api
        if not key:
            raise ValueError(
                "Provide an API key via .connect('KEY') or pass api='KEY'"
            )
        data = self.fred_logic.fetch_categories(_api=key)
        categories = data.get('categories', [])
        return pd.DataFrame(categories)

    def get_series_in_category(
        self,
        category_id: int,
        limit: int = 100,
        api: str = None,
    ) -> pd.DataFrame:
        key = api or self._api
        if not key:
            raise ValueError(
                "Provide an API key via .connect('KEY') or pass api='KEY'"
            )
        data = self.fred_logic.fetch_series_in_category(
            category_id=category_id, _api=key, limit=limit
        )
        return self.fred_logic.transform_search(data)

    @staticmethod
    def list_common_series() -> dict:
        return dict(COMMON_SERIES)
