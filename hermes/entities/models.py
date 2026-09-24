from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class EntityIdentifier:
    value: str
    source: str | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None


@dataclass(frozen=True)
class EntityAlias:
    value: str
    source: str | None = None


@dataclass(frozen=True)
class EntityRelationship:
    other_id: str
    kind: str


@dataclass
class Entity:
    id: str
    entity_type: str
    canonical_name: str
    country_id: str | None = None
    identifiers: dict[str, EntityIdentifier] = field(default_factory=dict)
    aliases: list[EntityAlias] = field(default_factory=list)
    relationships: list[EntityRelationship] = field(default_factory=list)
    attributes: dict = field(default_factory=dict)

    def lookup_keys(self) -> set[str]:
        """Everything this entity can be matched by: id, name, identifiers, aliases."""
        keys = {self.id, self.canonical_name}
        keys.update(i.value for i in self.identifiers.values())
        keys.update(a.value for a in self.aliases)
        return {k.lower() for k in keys if k}

    def __str__(self) -> str:
        return self.id


@dataclass
class EntityMatch:
    entity: Entity
    score: float
    match_type: str


__all__ = [
    "Entity",
    "EntityIdentifier",
    "EntityAlias",
    "EntityRelationship",
    "EntityMatch",
]