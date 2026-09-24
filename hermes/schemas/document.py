from hermes.schemas.base import FieldDef, Schema

DOCUMENT = Schema(
    name="document",
    version="1.0.0",
    namespace="document",
    fields=[
        FieldDef(name="document_id", type="str", required=True, semantic_type="id.document"),
        FieldDef(name="title", type="str", nullable=True, semantic_type="text.title"),
        FieldDef(name="source", type="str", required=True, semantic_type="source.name"),
        FieldDef(name="date", type="datetime", nullable=True, semantic_type="time.iso8601"),
        FieldDef(name="url", type="str", nullable=True, semantic_type="uri.url"),
        FieldDef(name="content_type", type="str", nullable=True, semantic_type="mime.type"),
        FieldDef(name="metadata", type="dict", nullable=True),
    ],
    primary_keys=["document_id"],
    description="Canonical document/filing.",
)