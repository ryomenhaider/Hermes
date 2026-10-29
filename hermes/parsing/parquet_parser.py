import io
from typing import Any, cast

try:
    import polars as pl
except ImportError:
    print("This Module Need Polars and PyArrow Installed, use pip/uv install/add hermes-plt[data] ")

from hermes.core.errors import ParseError


class ParquetParser:
    def parse(self, raw_data: object, **kwargs: object) -> pl.DataFrame:
        try:
            src = raw_data
            if isinstance(src, (bytes, bytearray)):
                src = io.BytesIO(src)
            return pl.read_parquet(cast(Any, src), **cast(Any, kwargs))
        except ParseError:
            raise
        except Exception as exc:
            raise ParseError(f"Failed to parse Parquet: {exc}") from exc
