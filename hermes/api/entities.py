from functools import lru_cache
from pathlib import Path

import polars as pl

from hermes.core.errors import HermesError, UnknownEntityTypeError
from hermes.core.hrm_id import hrm_id
from hermes.core.result import Result
from hermes.entities.models import Entity, EntityAlias, EntityIdentifier
from hermes.entities.registry import EntityRegistry
from hermes.entities.resolver import StaticEntityResolver
from hermes.resources.countries import countries_frame

_CIK_PATH = (
    Path(__file__).resolve().parent.parent / "connectors" / "lib" / "datasets" / "cik.parquet"
)

_TYPE_SYNONYMS = {
    "company": "company",
    "corporation": "company",
    "country": "country",
    "security": "security",
    "organization": "organization",
    "organisation": "organization",
    "person": "person",
}


@lru_cache(maxsize=1)
def _country_entities() -> list[Entity]:
    entities: list[Entity] = []
    for row in countries_frame().to_dicts():
        alpha3 = (row.get("alpha_3") or "").upper()
        name = row.get("name")
        if not alpha3 or not name:
            continue
        identifiers = {"iso3": EntityIdentifier(alpha3), "iso2": EntityIdentifier(str((row.get("alpha_2") or "")).upper())}
        aliases = [
            EntityAlias(value)
            for value in (str(v) for v in (row.get("official_name"), row.get("common_name")) if v)
            if value and value.lower() != name.lower()
        ]
        entities.append(
            Entity(
                id=hrm_id("country"),
                entity_type="country",
                canonical_name=name,
                identifiers=identifiers,
                aliases=list(aliases),
            )
        )
    return entities


@lru_cache(maxsize=1)
def _company_entities() -> list[Entity]:
    df = pl.read_parquet(_CIK_PATH)
    entities: list[Entity] = []
    for row in df.to_dicts():
        ticker = str(row.get("ticker") or "").strip()
        cik = str(row.get("cik_str") or "").strip()
        if not ticker or not cik:
            continue
        entities.append(
            Entity(
                id=hrm_id("company"),
                entity_type="company",
                canonical_name=ticker,
                identifiers={
                    "ticker": EntityIdentifier(ticker),
                    "cik": EntityIdentifier(cik, source="sec"),
                },
            )
        )
    return entities


@lru_cache(maxsize=1)
def get_registry() -> EntityRegistry:
    registry = EntityRegistry()
    companies = StaticEntityResolver(_company_entities(), entity_type="company")
    registry.register("company", companies)
    registry.register("organization", companies)
    registry.register("security", companies)
    registry.register("country", StaticEntityResolver(_country_entities(), entity_type="country"))
    registry.register("person", StaticEntityResolver([], entity_type="person"))
    return registry


def _success(entity: Entity) -> Result:
    return Result(status="success", data=entity, statistics={"entity_type": entity.entity_type, "id": entity.id})


def _failure(query: str, exc: Exception) -> Result:
    result = Result(status="failure")
    result.add_error(exc, query=query)
    return result


def resolve_entity(query: str, entity_type: str | None = None) -> Result:
    if entity_type is not None:
        entity_type = _TYPE_SYNONYMS.get(entity_type, entity_type)
    try:
        entity = get_registry().resolve(query, entity_type=entity_type)
    except UnknownEntityTypeError as exc:
        return _failure(query, exc)
    if entity is None:
        return _failure(query, HermesError(f"No entity found for {query!r}"))
    return _success(entity)


def resolve_country(query: str) -> Result:
    return resolve_entity(query, "country")


def resolve_company(query: str) -> Result:
    return resolve_entity(query, "company")


def resolve_security(query: str) -> Result:
    return resolve_entity(query, "security")


def resolve_organization(query: str) -> Result:
    return resolve_entity(query, "organization")


def resolve_person(query: str) -> Result:
    return resolve_entity(query, "person")