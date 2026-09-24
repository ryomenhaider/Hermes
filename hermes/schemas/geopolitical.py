from hermes.schemas.base import FieldDef, Schema

GEOPOLITICAL_EVENT = Schema(
    name="geopolitical.event",
    version="1.0.0",
    namespace="geopolitical",
    fields=[
        FieldDef(name="event_id", type="str", required=True, semantic_type="id.event"),
        FieldDef(name="date", type="datetime", required=True, semantic_type="time.iso8601"),
        FieldDef(name="event_type", type="str", required=True, semantic_type="code.event"),
        FieldDef(name="actor_1", type="str", nullable=True, semantic_type="code.actor"),
        FieldDef(name="actor_2", type="str", nullable=True, semantic_type="code.actor"),
        FieldDef(name="country", type="str", nullable=True, semantic_type="iso.country"),
        FieldDef(name="goldstein_scale", type="float", nullable=True, semantic_type="value.scale"),
        FieldDef(name="source", type="str", nullable=True, semantic_type="source.name"),
    ],
    primary_keys=["event_id"],
    description="Canonical geopolitical event.",
)