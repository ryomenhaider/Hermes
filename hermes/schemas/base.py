from pydantic import BaseModel


class FieldDef(BaseModel):
    name: str
    dtype: str
    nullable: bool = True
    required: bool = False
    description: str | None = None
    unit: str | None = None
    constraints: dict = {}


class Schema(BaseModel):
    name: str
    version: str
    fields: list[FieldDef] = []
    primary_keys: list[str] = []
    description: str | None = None

    def validate_data(self, data: object) -> None:
        raise NotImplementedError()

    def compatibility(self, other: "Schema") -> None:
        raise NotImplementedError()

    def field_names(self) -> list[str]:
        raise NotImplementedError()
