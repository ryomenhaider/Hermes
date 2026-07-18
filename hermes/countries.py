COUNTRY_META: dict[str, dict] = {
    "USA": {"name": "United States", "region": "North America", "income_group": "High income", "capital": "Washington, D.C.", "currency": "USD", "neighbors": ["CAN", "MEX"]},
    "CAN": {"name": "Canada", "region": "North America", "income_group": "High income", "capital": "Ottawa", "currency": "CAD", "neighbors": ["USA"]},
    "MEX": {"name": "Mexico", "region": "North America", "income_group": "Upper middle income", "capital": "Mexico City", "currency": "MXN", "neighbors": ["USA", "GTM", "BLZ"]},
    "GBR": {"name": "United Kingdom", "region": "Europe & Central Asia", "income_group": "High income", "capital": "London", "currency": "GBP", "neighbors": ["IRL"]},
    "DEU": {"name": "Germany", "region": "Europe & Central Asia", "income_group": "High income", "capital": "Berlin", "currency": "EUR", "neighbors": ["AUT", "BEL", "CZE", "DNK", "FRA", "LUX", "NLD", "POL", "CHE"]},
    "FRA": {"name": "France", "region": "Europe & Central Asia", "income_group": "High income", "capital": "Paris", "currency": "EUR", "neighbors": ["BEL", "DEU", "ITA", "LUX", "MCO", "ESP", "CHE"]},
    "JPN": {"name": "Japan", "region": "East Asia & Pacific", "income_group": "High income", "capital": "Tokyo", "currency": "JPY", "neighbors": []},
    "CHN": {"name": "China", "region": "East Asia & Pacific", "income_group": "Upper middle income", "capital": "Beijing", "currency": "CNY", "neighbors": ["AFG", "BTN", "MMR", "HKG", "IND", "KAZ", "PRK", "KGZ", "LAO", "MAC", "MNG", "PAK", "RUS", "TJK", "VNM"]},
    "IND": {"name": "India", "region": "South Asia", "income_group": "Lower middle income", "capital": "New Delhi", "currency": "INR", "neighbors": ["BGD", "BTN", "MMR", "CHN", "NPL", "PAK", "LKA"]},
    "BRA": {"name": "Brazil", "region": "Latin America & Caribbean", "income_group": "Upper middle income", "capital": "Brasília", "currency": "BRL", "neighbors": ["ARG", "BOL", "COL", "GUF", "GUY", "PRY", "PER", "SUR", "URY", "VEN"]},
    "RUS": {"name": "Russia", "region": "Europe & Central Asia", "income_group": "Upper middle income", "capital": "Moscow", "currency": "RUB", "neighbors": ["AZE", "BLR", "CHN", "EST", "FIN", "GEO", "KAZ", "PRK", "LVA", "LTU", "MNG", "NOR", "POL", "UKR"]},
    "ZAF": {"name": "South Africa", "region": "Sub-Saharan Africa", "income_group": "Upper middle income", "capital": "Pretoria", "currency": "ZAR", "neighbors": ["AGO", "BWA", "LSO", "MOZ", "NAM", "SWZ", "ZWE"]},
    "UKR": {"name": "Ukraine", "region": "Europe & Central Asia", "income_group": "Lower middle income", "capital": "Kyiv", "currency": "UAH", "neighbors": ["BLR", "HUN", "MDA", "POL", "ROU", "RUS", "SVK"]},
}


def get_country_metadata(country: str) -> dict | None:
    return COUNTRY_META.get(country.upper())


def list_countries() -> list[dict]:
    return [
        {"iso_code": code, "name": meta["name"], "region": meta["region"]}
        for code, meta in sorted(COUNTRY_META.items())
    ]


def get_region(country: str) -> str:
    meta = COUNTRY_META.get(country.upper())
    return meta["region"] if meta else "Unknown"


def get_income_group(country: str) -> str:
    meta = COUNTRY_META.get(country.upper())
    return meta["income_group"] if meta else "Unknown"
