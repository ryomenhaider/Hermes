from hermes.schemas.base import FieldDef, Schema

ENTITY = Schema(
    name="entity",
    version="1.0.0",
    namespace="entity",
    fields=[
        FieldDef(name="entity_id", type="str", required=True, semantic_type="id.hrm"),
        FieldDef(name="name", type="str", required=True, semantic_type="text.name"),
        FieldDef(name="entity_type", type="str", required=True, semantic_type="entity.type"),
        FieldDef(name="country", type="str", nullable=True, semantic_type="iso.country"),
        FieldDef(name="identifiers", type="dict", nullable=True, semantic_type="identifier.set"),
        FieldDef(name="aliases", type="list", nullable=True, semantic_type="text.alias"),
    ],
    primary_keys=["entity_id"],
    description="Canonical entity.",
)