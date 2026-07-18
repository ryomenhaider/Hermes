from dataclasses import dataclass


@dataclass
class IndicatorRecord:
    date: str = "datetime64[ns]"
    country: str = ""
    indicator: str = ""
    value: float = 0.0
    source: str = ""
