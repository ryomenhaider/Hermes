from hermes.schemas.base import FieldDef, Schema

FINANCIAL_OBSERVATION = Schema(
    name="financial.observation",
    version="1.0.0",
    namespace="financial",
    fields=[
        FieldDef(name="entity_id", type="str", required=True, semantic_type="id.hrm"),
        FieldDef(name="date", type="datetime", required=True, semantic_type="time.iso8601"),
        FieldDef(name="metric", type="str", required=True, semantic_type="code.metric"),
        FieldDef(name="value", type="float", nullable=True, semantic_type="value.monetary"),
        FieldDef(name="unit", type="str", nullable=True, semantic_type="unit.monetary"),
        FieldDef(name="period", type="str", nullable=True, semantic_type="code.period"),
        FieldDef(name="source", type="str", nullable=True, semantic_type="source.name"),
    ],
    primary_keys=["entity_id", "date", "metric"],
    description="Canonical financial observation.",
)