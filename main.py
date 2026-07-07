from src.hermes.connectors.fred.connector import FredConnector
from src.hermes.database.database import init_db
from src.hermes.api.server import app
from src.hermes.config import HOST, PORT, ENV
import uvicorn

fred_connector = FredConnector('observations')

def main():
    print('='*50)
    print('              HERMES HAS STARTED')
    print('='*50)

    print('='*50)
    print('              Data Migration HAS STARTED')
    print('='*50)

    init_db()

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
        app=app,
        host=HOST,
        port=PORT,
        reload=ENV,
    )

if __name__ == '__main__':
    main()