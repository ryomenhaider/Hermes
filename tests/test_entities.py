import pytest

import hermes as hr
from hermes.core.hrm_id import hrm_id
from hermes.entities.models import Entity, EntityIdentifier
from hermes.entities.registry import EntityRegistry
from hermes.entities.resolver import StaticEntityResolver


def _nvidia() -> Entity:
    return Entity(
        id=hrm_id("company"),
        entity_type="company",
        canonical_name="NVDA",
        identifiers={"ticker": EntityIdentifier("NVDA"), "cik": EntityIdentifier("1045810", source="sec")},
        aliases=[],
    )


def test_static_resolver_resolves_by_any_identifier():
    resolver = StaticEntityResolver([_nvidia()])
    assert resolver.resolve("AAPL") is None
    for query in ("nvda", "NVDA", "1045810"):
        assert resolver.resolve(query) is not None
    scores = resolver.match("nvda")
    assert scores and scores[0].score == 1.0


def test_static_resolver_fuzzy_match():
    resolver = StaticEntityResolver([_nvidia()])
    fuzzy = resolver.match("nvdia", threshold=0.7)
    assert fuzzy and fuzzy[0].match_type == "fuzzy"


def test_entity_registry_dispatch():
    registry = EntityRegistry()
    companies = StaticEntityResolver([_nvidia()])
    registry.register("company", companies)
    registry.register("person", StaticEntityResolver([]))
    assert registry.list_types() == ["company", "person"]
    assert registry.resolve("1045810", "company").canonical_name == "NVDA"
    assert registry.resolve("1045810").entity_type == "company"
    assert registry.resolve("nobody", "company") is None
    with pytest.raises(Exception):
        registry.resolve("x", "bank")


def test_hr_resolve_country():
    result = hr.resolve_country("USA")
    assert result.is_success()
    assert result.data.entity_type == "country"
    assert result.data.identifiers["iso2"].value == "US"
    assert hr.resolve_country("zzzz").errors[0].code == "HermesError"


def test_hr_resolve_company():
    result = hr.resolve_company("AAPL")
    assert result.is_success()
    assert result.data.entity_type == "company"
    assert result.data.identifiers["cik"].value == "320193"
    assert hr.resolve_company("NOTATICKER").errors[0].code == "HermesError"


def test_hr_resolve_entity_unknown_type():
    result = hr.resolve_entity("x", "bank")
    assert not result.is_success()
    assert result.errors[0].code == "UnknownEntityTypeError"