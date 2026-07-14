import httpx
import pandas as pd

class AlphaVLogic:

    def fetch_stocks(
            self,
            function: str,
            symbol: str,
            api: str      
        ):

        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={api}'

        r = httpx.get(url)

        data = r.content

        data = data.decode()

        return data
    
    def validate_stocks(self, data):

        meta_data = data["Meta Data"]

        for key, value in data.items():
            pass
    
    def transform_stocks(self, data):
        
        df = pd.read_json(data)

        d = df['Time Series (Daily)']
        