from dataclasses import dataclass
from typing import date

@dataclass
class indicator:
    date = 'datetime64[ns]'
    country_iso3: str
    indicator_id: str
    value:  float
    source: str

