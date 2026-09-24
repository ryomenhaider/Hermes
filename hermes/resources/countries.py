from functools import lru_cache
from pathlib import Path

import polars as pl

from hermes.normalization.constants import _COUNTRY_COMMON_ALIASES

COUNTRIES_PATH = Path(__file__).resolve().parent / "countries.parquet"


@lru_cache(maxsize=1)
def _countries() -> pl.DataFrame:
    return pl.read_parquet(COUNTRIES_PATH)


@lru_cache(maxsize=1)
def iso3_index() -> dict[str, str]:
    return {
        row["alpha_3"].upper(): row["alpha_2"]
        for row in _countries().to_dicts()
        if row.get("alpha_3") and row.get("alpha_2")
    }


@lru_cache(maxsize=1)
def country_aliases() -> dict[str, str]:
    """Map any common name, official name, and ISO code onto its ISO alpha-2."""
    aliases: dict[str, str] = {}
    for row in _countries().to_dicts():
        alpha2 = row.get("alpha_2")
        if not alpha2:
            continue
        for field in ("alpha_2", "alpha_3", "name", "official_name", "common_name"):
            value = row.get(field)
            if isinstance(value, str) and value:
                aliases[value.casefold()] = alpha2
    aliases.update(_COUNTRY_COMMON_ALIASES)
    return aliases


def iso3_to_iso2(iso3_code: str) -> str:
    return iso3_index().get(iso3_code.upper(), "Not Found")


def check_iso3(code: str) -> None:
    if code.upper() not in iso3_index():
        raise ValueError(f"{code!r} is not a valid ISO-3166 alpha-3 code")


__all__ = ["iso3_to_iso2", "check_iso3", "country_aliases", "iso3_index", "COUNTRIES_PATH"]