class FredMapper:

    def map_metadata(self, data):

        return {
            'id': data['id'],
            'title': data['title'],
            'frequency': data['frequency'],
            'units': data['units'],
            'source': 'FRED'
        }
    
    def map_obs(self, data: list[dict], series_id: str | None = None) -> list[dict]:

        return [
            {
                "series_id": series_id,
                "period": obs["date"],
                "value": float(obs["value"]),
            }
            for obs in data
        ]
    
    def map(self, data, endpoint, series_id: str | None = None):

        if endpoint == 'observations':
            return self.map_obs(data, series_id=series_id)
        
        elif endpoint == 'metadata':
            return self.map_metadata(data)
        
        raise ValueError(f'Unknown Endpoint {endpoint}')