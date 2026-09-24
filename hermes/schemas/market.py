from hermes.schemas.base import FieldDef, Schema

MARKET_OBSERVATION = Schema(
    name="market.observation",
    version="1.0.0",
    namespace="market",
    fields=[
        FieldDef(name="symbol", type="str", required=True, semantic_type="code.instrument"),
        FieldDef(name="timestamp", type="datetime", required=True, semantic_type="time.iso8601"),
        FieldDef(name="open", type="float", nullable=True, semantic_type="value.monetary"),
        FieldDef(name="high", type="float", nullable=True, semantic_type="value.monetary"),
        FieldDef(name="low", type="float", nullable=True, semantic_type="value.monetary"),
        FieldDef(name="close", type="float", nullable=True, semantic_type="value.monetary"),
        FieldDef(name="volume", type="float", nullable=True, semantic_type="value.count"),
        FieldDef(name="source", type="str", nullable=True, semantic_type="source.name"),
    ],
    primary_keys=["symbol", "timestamp"],
    description="Canonical market observation (OHLCV).",
)