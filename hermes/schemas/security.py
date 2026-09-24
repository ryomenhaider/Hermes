from hermes.schemas.base import FieldDef, Schema

SECURITY_EVENT = Schema(
    name="security.event",
    version="1.0.0",
    namespace="security",
    fields=[
        FieldDef(name="event_id", type="str", required=True, semantic_type="id.event"),
        FieldDef(name="date", type="datetime", required=True, semantic_type="time.iso8601"),
        FieldDef(name="event_type", type="str", required=True, semantic_type="code.event"),
        FieldDef(name="country", type="str", nullable=True, semantic_type="iso.country"),
        FieldDef(name="severity", type="str", nullable=True, semantic_type="code.severity"),
        FieldDef(name="description", type="str", nullable=True, semantic_type="text.description"),
        FieldDef(name="source", type="str", nullable=True, semantic_type="source.name"),
    ],
    primary_keys=["event_id"],
    description="Canonical security event.",
)