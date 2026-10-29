"""
# Method  Endpoint                                      Purpose
# ------  --------------------------------------------  ----------------------------
# GET     /lei-records                                  Search and filter LEI records
# GET     /lei-records/{lei}                            Retrieve a specific LEI record
# GET     /lei-records/{lei}/direct-parent              Find the reported direct parent
# GET     /lei-records/{lei}/ultimate-parent            Find the reported ultimate parent
# GET     /lei-records/{lei}/direct-children            Find direct subsidiaries
# GET     /lei-records/{lei}/ultimate-children          Find ultimate subsidiaries
# GET     /lei-records/{lei}/lei-issuer                 Retrieve the LEI issuer
# GET     /lei-records/{lei}/managing-lou               Retrieve the managing LOU
# GET     /lei-records/{lei}/isins                      Retrieve associated ISIN information
# GET     /fuzzycompletions                             Fuzzy search and autocomplete
# GET     /autocompletions                              Autocomplete suggestions
# GET     /lei-issuers                                  List LEI issuers
# GET     /entity-legal-forms/{code}                    Retrieve legal-form information
# GET     /registration-authorities/{code}              Retrieve registration-authority information
# GET     /countries                                    Retrieve country reference data
# GET     /fields                                       Discover searchable fields and filter operators
"""


from hermes.connectors.base import BaseConnector

class GLEIF(BaseConnector):

    def __init__(self, cache = None, *, retry_auth = False, headers = None):
        super().__init__(cache, retry_auth=retry_auth, headers=headers)
        self._url = "https://api.gleif.org/api/v1"

    def get_lei(self, company: str) -> list[dict[str, str]]:
        url = f"{self._url}/lei-records"
        params = {
            "filter[entity.legalName]": f"{company}",
            "page[size]": 10,
        }
        response = self._get_json(url=url, params=params, headers=self._headers)
        data = []
        for record in response["data"]:
            entity = record["attributes"]["entity"]
            data.append({
                "lei": record["id"],
                "legal_name": entity["legalName"]["name"],
                "country": entity.get("legalAddress", {}).get("country"),
                "status": entity.get("status"),
            })

        return data
    

if __name__ == "__main__":
    gleif = GLEIF()
    gleif.get_lei("apple")