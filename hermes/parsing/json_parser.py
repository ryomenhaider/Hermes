import io
from pathlib import Path
from typing import Any, cast

try:
    import polars as pl
except ImportError:
    print("This Module Need Polars and PyArrow Installed, use pip/uv install/add hermes-plt[data] ")

from hermes.core.errors import ParseError


class JSONParser:
    def parse(self, raw_data: object, **kwargs: object) -> pl.DataFrame:
        try:
            src = raw_data
            if isinstance(src, (bytes, bytearray)):
                src = io.BytesIO(bytes(src))
            elif isinstance(src, str) and ("\n" in src or src.lstrip().startswith(("{", "["))):
                src = io.BytesIO(src.encode())
            if self._is_jsonl(src):
                return pl.read_ndjson(cast(Any, src), **cast(Any, kwargs))
            return pl.read_json(cast(Any, src), **cast(Any, kwargs))
        except ParseError:
            raise
        except Exception as exc:
            raise ParseError(f"Failed to parse JSON: {exc}") from exc

    @staticmethod
    def _is_jsonl(source: object) -> bool:
        if isinstance(source, Path):
            return source.suffix.lower() in (".jsonl", ".ndjson")
        if isinstance(source, io.BytesIO):
            source = source.getvalue()
        if isinstance(source, (bytes, bytearray)):
            source = bytes(source).decode(errors="replace")
        if isinstance(source, str) and source.rstrip().lower().endswith((".jsonl", ".ndjson")):
            return True
        text = str(source).lstrip()
        lines = [line for line in text.splitlines() if line.strip()]

        return len(lines) > 1 and all(line.lstrip().startswith("{") for line in lines)
