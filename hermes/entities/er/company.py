"""
A company must have this data;
{
    "{company}": {
        "name": "",
        "legalName": "",
        "aliases": "",
        "country": "",
        "jurisdiction": "",
        "lei": "",
        "cik": "",
        "permid": "",
        "wikidata_id": "",
        "website": "",
        "listing": "",
        "securities": "",
        "industry_code": ""
    }
}
"""
def identifier(company: str):
    ...

class Company:

    def __init__(self, company_name: str):
        self.company = company_name


    @property
    def candles(self):
        ...
    @property
    def market_data(self):
        ...
    @property
    def news(self):
        ...
    @property
    def financials(self):
        ...
    @property
    def profile(self):
        ...
    @property
    def filings(self):
        ...
    @property
    def ownership(self):
        ...
    @property
    def corporate_action(self):
        ...
    @property
    def relations(self):
        ...
    