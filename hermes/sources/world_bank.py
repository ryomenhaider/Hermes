import httpx
import pandas as pd
import pycountry
import re
import time
import logging

logger = logging.getLogger(__name__)

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
        
        # when you realize you have free will !
        is_date_range_correct = is_valid_range(date_range=date_range)

        if is_date_range_correct != True:
            raise ValueError('The Date range should be in XXXX:XXXX format')

        if frequency and frequency not in ("Q", "M", "Y"):
            raise ValueError("frequency must be one of 'Q' (quarterly), 'M' (monthly), or 'Y' (yearly)")

        base_url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"

        params = {
            "format": "json",
            "per_page": per_page,
        }

        # date_range and most_recent (mrv) are mutually exclusive in the API;
        # prefer mrv if both are somehow supplied.
        if most_recent:
            params["mrv"] = most_recent
        elif date_range:
            params["date"] = date_range

        # frequency only takes effect alongside mrv per the World Bank docs
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
        
    def validate_worldbank(self, item: dict) -> bool:
        
        required = {"indicator", "country", "countryiso3code", "date", "value"}
        
        if not required.issubset(item):
            return False
        if not isinstance(item["indicator"], dict) or "id" not in item["indicator"]:
            return False
        if not isinstance(item["country"], dict) or "id" not in item["country"]:
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

        # drop rows where World Bank has no data for that period
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




class World_Bank:

    def __init__(self):
        self.wb = WBLogic()

    def get_indicators(self):

        url = "https://api.worldbank.org/v2/indicator?format=json&per_page=10000"
        r = httpx.get(url)
        r.raise_for_status()

        r = r.json()
        
        dat = r[1]
        
        data = []

        for d in dat:
            data.append(
                {
                    "indicator_code": d['id'],
                    "name": d['name'],
                    "unit": d['unit'],
                    "description": d['sourceNote'],
                    "source": d['source']['value'] 
                }
            )

        return data
    
    def get_countries(self):
        url = 'https://api.worldbank.org/v2/country?format=json&per_page=300'

        r = httpx.get(url)
        r.raise_for_status()

        return r.json()
    
    def get_country_info(self, country: str):
        
        if pycountry.countries.lookup(country).alpha_3 != country.upper():
            raise LookupError('The Country should be in iso3')
        
        url = f"https://api.worldbank.org/v2/country/{country}?format=json"

        r = httpx.get(url)
       
        r.raise_for_status()
        r = r.json()

        data = r[1]
        return data

    def world_bank_data(
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
            
            if export == True:
                self.wb.export(transformed_data, filetype=filetype)
                return transformed_data
            
            return transformed_data
        
        else:
            raise RuntimeError('The Data is not valid for application')
