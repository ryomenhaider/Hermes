import httpx
import pandas as pd
import pycountry
import re
import time
import logging

logger = logging.getLogger(__name__)

WB_BASE = 'https://api.worldbank.org/v2'


def is_valid_range(date_range):
    pattern = r"^\d{4}:\d{4}$"
    return bool(re.match(pattern, date_range))


class WBLogic:

    def fetch_worldbank(
        self,
        indicator: str,
        country: str = "all",
        date_range: str = None,
        most_recent: int = None,
        frequency: str = None,
        per_page: int = 10000,
    ) -> list[dict]:

        is_date_range_correct = is_valid_range(date_range=date_range)

        if is_date_range_correct is not True:
            raise ValueError('The Date range should be in XXXX:XXXX format')

        if frequency and frequency not in ("Q", "M", "Y"):
            raise ValueError("frequency must be one of 'Q' (quarterly), 'M' (monthly), or 'Y' (yearly)")

        base_url = f"{WB_BASE}/country/{country}/indicator/{indicator}"

        params = {
            "format": "json",
            "per_page": per_page,
        }

        if most_recent:
            params["mrv"] = most_recent
        elif date_range:
            params["date"] = date_range

        if frequency:
            if not most_recent:
                raise ValueError("frequency requires most_recent (mrv) to be set")
            params["frequency"] = frequency

        all_records = []
        page = 1

        while True:
            params["page"] = page
            response = httpx.get(base_url, params=params, timeout=30)
            response.raise_for_status()

            payload = response.json()

            if isinstance(payload, dict) or "message" in payload[0]:
                message = payload[0].get("message", [{"value": "Unknown World Bank API error"}])
                raise ValueError(message[0]["value"])

            metadata, records = payload

            if not records:
                break

            all_records.extend(records)

            if page >= metadata.get("pages", 1):
                break

            page += 1

        return all_records

    def validate_worldbank(self, data: list[dict]) -> bool:
        if not isinstance(data, list):
            logger.error('Data must be a list of records')
            return False

        required = {"indicator", "country", "countryiso3code", "date", "value"}

        for item in data:
            if not required.issubset(item):
                logger.warning(f'Record missing required fields: {required - set(item)}')
                return False
            if not isinstance(item["indicator"], dict) or "id" not in item["indicator"]:
                logger.warning('Record missing indicator.id')
                return False
            if not isinstance(item["country"], dict) or "id" not in item["country"]:
                logger.warning('Record missing country.id')
                return False

        return True

    def _parse_wb_date(self, date_str: str):
        date_str = str(date_str)

        if "Q" in date_str:
            return pd.Period(date_str, freq="Q")
        if "M" in date_str:
            return pd.Period(date_str, freq="M")
        return pd.Period(date_str, freq="Y")

    def transform(self, data: list[dict]) -> pd.DataFrame:
        if not data:
            return pd.DataFrame(
                columns=["country", "country_iso3", "indicator_id", "indicator_name", "date", "value"]
            )

        df = pd.json_normalize(data)

        df = df.rename(
            columns={
                "country.value": "country",
                "countryiso3code": "country_iso3",
                "indicator.id": "indicator_id",
                "indicator.value": "indicator_name",
            }
        )

        df = df[["country", "country_iso3", "indicator_id", "indicator_name", "date", "value"]]

        df = df.dropna(subset=["value"])

        df["date"] = df["date"].apply(self._parse_wb_date)

        df = df.sort_values(["country", "date"]).reset_index(drop=True)

        return df

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

    def fetch_metadata(self, indicator_code: str) -> dict:
        url = f'{WB_BASE}/indicator/{indicator_code}?format=json'
        resp = httpx.get(url)
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, list) and len(data) > 1 and data[1]:
            return data[1][0]
        raise ValueError(f'No metadata found for indicator {indicator_code}')

    def fetch_topics(self) -> list[dict]:
        url = f'{WB_BASE}/topic?format=json&per_page=100'
        resp = httpx.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data[1] if isinstance(data, list) and len(data) > 1 else []

    def fetch_countries_by(self, region: str = None, income_level: str = None) -> list[dict]:
        if region:
            url = f'{WB_BASE}/region/{region}/country?format=json&per_page=500'
        elif income_level:
            url = f'{WB_BASE}/incomelevel/{income_level}/country?format=json&per_page=500'
        else:
            url = f'{WB_BASE}/country?format=json&per_page=300'
        resp = httpx.get(url)
        resp.raise_for_status()
        data = resp.json()
        return data[1] if isinstance(data, list) and len(data) > 1 else []


class World_Bank:

    def __init__(self):
        self.wb = WBLogic()
    
    def get_indicators(self):
        url = f"{WB_BASE}/indicator?format=json&per_page=10000"
        r = httpx.get(url)
        r.raise_for_status()
        r = r.json()
        dat = r[1]
        data = []

        for d in dat:
            data.append({
                "indicator_code": d['id'],
                "name": d['name'],
                "unit": d['unit'],
                "description": d['sourceNote'],
                "source": d['source']['value']
            })
        
        return data

    def search_indicators(self, query: str) -> list[dict]:
        query = query.lower()
        all_indicators = self.get_indicators()
        return [
            ind for ind in all_indicators
            if query in ind['name'].lower() or query in ind['indicator_code'].lower()
        ]

    def get_indicator_metadata(self, indicator_code: str) -> dict:
        return self.wb.fetch_metadata(indicator_code)

    def get_topics(self) -> list[dict]:
        return self.wb.fetch_topics()

    def get_countries(self):
        url = f'{WB_BASE}/country?format=json&per_page=300'
        r = httpx.get(url)
        r.raise_for_status()
        return r.json()

    def get_country_info(self, country: str):
        if pycountry.countries.lookup(country).alpha_3 != country.upper():
            raise LookupError('The Country should be in iso3')
        url = f"{WB_BASE}/country/{country}?format=json"
        r = httpx.get(url)
        r.raise_for_status()
        r = r.json()
        data = r[1]
        return data

    def get_countries_by_region(self, region_code: str) -> list[dict]:
        return self.wb.fetch_countries_by(region=region_code)

    def get_countries_by_income(self, income_level: str) -> list[dict]:
        return self.wb.fetch_countries_by(income_level=income_level)

    def get_data(
        self,
        indicator: str,
        country: str = "all",
        date_range: str = None,
        most_recent: int = None,
        frequency: str = None,
        per_page: int = 10000,
        export: bool | None = None,
        filetype: str = 'json'
    ):
        data = self.wb.fetch_worldbank(
            indicator=indicator,
            country=country,
            date_range=date_range,
            most_recent=most_recent,
            frequency=frequency,
            per_page=per_page
        )

        vl = self.wb.validate_worldbank(data=data)

        if vl:
            transformed_data = self.wb.transform(data=data)

            if export is True:
                self.wb.export(transformed_data, filetype=filetype)
                return transformed_data

            return transformed_data

        raise RuntimeError('The Data is not valid for application')

    def get_multiple_indicators(
        self,
        indicators: list[str],
        country: str = "all",
        date_range: str = None,
        most_recent: int = None,
        frequency: str = None,
        per_page: int = 10000,
        export: bool | None = None,
        filetype: str = 'json',
    ) -> pd.DataFrame:
    
        frames = {}
        for code in indicators:
            raw = self.wb.fetch_worldbank(
                indicator=code,
                country=country,
                date_range=date_range,
                most_recent=most_recent,
                frequency=frequency,
                per_page=per_page,
            )
            vl = self.wb.validate_worldbank(data=raw)
            if vl:
                df = self.wb.transform(data=raw)
                frames[code] = df.set_index(['country', 'date'])['value']

        result = pd.concat(frames, axis=1)
        result.columns.name = 'indicator'

        if export is True:
            self.wb.export(result.reset_index(), filetype=filetype)

        return result
