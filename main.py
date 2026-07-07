from src.hermes.connectors.fred.connector import FredConnector

fred_connector = FredConnector('observations')

def main():
    fred_connector.fetch()
    fred_connector.validate()
    fred_connector.mapper()
    fred_connector.store()