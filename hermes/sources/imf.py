import httpx
import pandas as pd
import logging
import json, time
logger = logging.getLogger(__name__)


class IMFLogic:
    def __init__(self):
        self.url = "https://www.imf.org/external/datamapper/api/v1"

    def fetch_imf_datamapper(
        self, 
        indicator: str, 
        country: str, 

    ):
    
        try:
            url = f"{self.url}/{indicator}"
                
            r = httpx.get(url)
            r.raise_for_status()
            raw_data = r.json()
            
            indicator_data = raw_data.get("values", {}).get(indicator, {})
            country_data = indicator_data.get(country, {})

            df = pd.Series(country_data, name="Value").to_frame()
            df.index.name = "Year"
            
            return indicator, country, df
            
        except httpx.HTTPError as e:
            raise httpx.HTTPError(f"API request failed: {e}")

    def transform(
        self,
        data: json,
        indicator: str,
        country: str
    ) -> pd.DataFrame:
        

        df = []
        d = data['Value']
        for i, j in d.items():
            date = pd.to_datetime(i)
            value = pd.to_numeric(j)
            df.append(
                {
                    "date": date,
                    "country_iso3": country,
                    "indicator_id": indicator,
                    "value": value,
                    "source": 'IMF'
                }
            )
        df = pd.DataFrame(df)
        df = df.set_index('date')
        return df

    def validate(
        self,
        data: pd.DataFrame
    ) -> bool:
        
        data = data.to_dict(orient='records')
        required = {"indicator", "country", "countryiso3code", "date", "value"}

        for item in data:
            
            if not required.issubset(item):
                logger.warning(f'Record missing required fields: {required - set(item)}')
                return False
            
        return True
    
    def export(self, data: pd.DataFrame, filetype: str) -> str:
        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        ts = time.time()
        path = f'data/world_bank{ts}.{filetype}'

        if filetype == 'json':
            import json
            # Convert to plain Python records to bypass ujson's strict recursion limits
            records = data.reset_index().to_dict(orient='records')
            with open(path, 'w', encoding='utf-8') as f:
                # default=str handles datetime/Timestamp fields gracefully if they aren't fully localized
                json.dump(records, f, default=str)
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
class IMF:

    def __init__(self):
        self.imf = IMFLogic()
    
    def get_indicators(self) -> list[str, dict]:
        
        url = f'{self.imf.url}/indicators'
        r = httpx.get(url=url)
        r = r.json()
        indicators = r['indicators']
        data = ['indicators']
        for i, j in indicators.items():
            data.append(
                {
                    "Name": i,
                    "Label": j['label'],
                    "description": j['description']
                }
            )

        return data
    
    def get_countries(self) -> list[str, dict]:
        
        url = f'{self.imf.url}/countries'
        r = httpx.get(url)
        r = r.json()
        
        countries = r['countries']
        data = ['countries']
        for i, j in countries.items():
            data.append(
                {
                    i : j['label']
                }
            )
        return data

    def get_regions(self) -> list[str, dict]:
        
        url = f'{self.imf.url}/regions'
        r = httpx.get(url)
        r = r.json()
        
        regions = r['regions']
        data = ['regions']
        for i, j in regions.items():
            data.append(
                {
                    i : j['label']
                }
            )
        return data

    def get_groups(self) -> list[str, dict]:
        
        url = f'{self.imf.url}/regions'
        r = httpx.get(url)
        r = r.json()
        
        regions = r['groups']
        data = ['groups']
        for i, j in regions.items():
            data.append(
                {
                    i : j['label']
                }
            )
        return data
    
    def get_data(
        self,
        indicator: str,
        country: str,
        export: bool = False,
        filetype: str = 'csv'
    ):
        try:
            data = self.imf.fetch_imf_datamapper(
                indicator=indicator,
                country=country
            )

            transformed_data = self.imf.transform(
                data=data,
                indicator=indicator,
                country=country
            )

            vl = self.imf.validate(transformed_data)
            
            if vl:
                logger.info('data is valided')
                if export:
                    exprt = self.imf.export(transformed_data, filetype=filetype)
                    return transformed_data
                else:
                    return transformed_data
            else:
                logger.error('The data is not validated')
                return transformed_data
            
        except Exception as e:
            raise RuntimeError(f'Error: {e}')
    
    def get_multiple_data(
        self,
        indicators: list[str],
        countries: list[str],
        export: bool = False,
        filetype: str = 'csv'    
    ): 
        try:
            all_dfs = []
            for indicator in indicators:
                for country in countries:
                    result = self.get_data(
                        indicator=indicator,
                        country=country,
                        export=export,
                        filetype=filetype
                    )
                    
                    if result is not None and not result.empty:
                        all_dfs.append(result)
            
            if all_dfs:
                import pandas as pd
                combined_df = pd.concat(all_dfs, ignore_index=True)
                return combined_df
            else:
                import pandas as pd
                return pd.DataFrame()
            
        except Exception as e:
            raise RuntimeError(f'Error gathering multiple datasets: {e}')


if __name__ == "__main__":
    
    imf = IMFLogic()
    filtered_data = imf.fetch_imf_datamapper(
        indicator='NGDPD',
        country='PAK',
        start_date=2000,
        end_date=2020
    )
    
    transformed_data = imf.transform(
        data=filtered_data,
        indicator='NGDPD',
        country='PAK'
    )
    
    transformed_data.to_csv('data/imf.csv')