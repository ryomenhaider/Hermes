class FredMapper:

    def map_metadata(self, data):

        return {
            'code': data['id'],
            'title': data['title'],
            'frequency': data['frequency'],
            'units': data['units'],
            'Source': 'FRED'
        }
    
    def map_obs(self, data):

        return [
            {
                "period": obs["date"],
                "value": float(obs["value"]),
            }
            for obs in data
        ]
    
    def map(self, data, endpoint):

        if endpoint == 'observation':
            return self.map_obs(data)
        
        elif endpoint == 'metadata':
            return self.map_metadata(data)
        
        raise ValueError(f'Unknown Endpoint {endpoint}')