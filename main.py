from src.hermes.connectors.fred.connector import FredConnector
from src.hermes.database.database import init_db
from src.hermes.config import HOST, PORT, ENV, SUPABASE_DB_URL
import uvicorn

def main():
    fred_connector = FredConnector('observations')

    print('='*50)
    print('              HERMES HAS STARTED')
    print('='*50)

    print('='*50)
    print('              RUNNING HERMES DB')
    print('='*50)
    
    init_db(SUPABASE_DB_URL)
    
    print('='*50)
    print('              RUNNING HERMES MAIN LOGIC')
    print('='*50)

    fred_connector.fetch()
    fred_connector.validate()
    fred_connector.mapper()
    fred_connector.store()

    print('='*50)
    print('              RUNNING HERMES MAIN API')
    print('='*50)

    uvicorn.run(
        "src.hermes.api.server:app",
        host=HOST,
        port=int(PORT),
        reload=(ENV == "dev"),
    )

if __name__ == '__main__':
    main()