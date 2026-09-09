from pydantic import BaseModel, Field


class Constraint(BaseModel):
    field: str
    constraint_type: str
    params: dict = {}


class DataContract(BaseModel):
    schema_name: str | None = Field(default=None, alias="schema")
    required_columns: list[str] = []
    constraints: list[Constraint] = []
    description: str | None = None
