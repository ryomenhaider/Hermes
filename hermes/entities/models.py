from pydantic import BaseModel


class Entity(BaseModel):
    id: str
    name: str
    entity_type: str
    country: str | None = None
    identifiers: dict[str, str] = {}
    aliases: list[str] = []
    metadata: dict = {}


class EntityMatch(BaseModel):
    entity: Entity
    score: float
    match_type: str
