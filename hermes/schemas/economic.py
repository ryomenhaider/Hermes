from hermes.schemas.base import FieldDef, Schema

ECONOMIC_OBSERVATION = Schema(
    name="economic.observation",
    version="1.0.0",
    namespace="economic",
    fields=[
        FieldDef(name="entity_id", type="str", required=True, semantic_type="id.hrm"),
        FieldDef(name="date", type="datetime", required=True, semantic_type="time.iso8601"),
        FieldDef(name="indicator", type="str", required=True, semantic_type="code.indicator"),
        FieldDef(name="value", type="float", nullable=True, semantic_type="value.measure"),
        FieldDef(name="unit", type="str", nullable=True, semantic_type="unit.measure"),
        FieldDef(name="frequency", type="str", nullable=True, semantic_type="code.frequency"),
        FieldDef(name="source", type="str", nullable=True, semantic_type="source.name"),
    ],
    primary_keys=["entity_id", "date", "indicator"],
    description="Canonical economic observation.",
)