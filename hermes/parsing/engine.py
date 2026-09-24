from pathlib import Path
from typing import Any

import polars as pl

from hermes.core.errors import ParseError
from hermes.parsing.csv_parser import CSVParser
from hermes.parsing.json_parser import JSONParser
from hermes.parsing.parquet_parser import ParquetParser
from hermes.parsing.xml_parser import XMLParser

_FORMAT_EXTENSIONS = {
    ".csv": "csv",
    ".json": "json",
    ".jsonl": "jsonl",
    ".ndjson": "jsonl",
    ".parquet": "parquet",
    ".xml": "xml",
}

_SUPPORTED_FORMATS = frozenset(["csv", "json", "jsonl", "parquet", "xml"])


class ParserEngine:
    def __init__(self) -> None:
        self._parsers: dict[str, Any] = {
            "csv": CSVParser(),
            "json": JSONParser(),
            "jsonl": JSONParser(),
            "parquet": ParquetParser(),
            "xml": XMLParser(),
        }

    def detect_format(self, source: object) -> str | None:
        if isinstance(source, Path):
            return _FORMAT_EXTENSIONS.get(source.suffix.lower())
        if isinstance(source, str):
            suffix = _FORMAT_EXTENSIONS.get(Path(source).suffix.lower())
            if suffix is not None:
                return suffix
            first = source.lstrip()[:1]
            if first == "<":
                return "xml"
            if first in ("{", "["):
                return "json"

            return None
        if isinstance(source, (bytes, bytearray)):
            first_byte = bytes(source).lstrip()[:1]
            if first_byte == b"<":
                return "xml"
            if first_byte in (b"{", b"["):
                return "json"
            return None
        return None

    def parse(self, raw_data: object, format: str | None = None, **kwargs: object) -> pl.DataFrame:
        fmt = format or self.detect_format(raw_data)
        if fmt is None:
            raise ParseError(f"Unsupported or undetectable format for {type(raw_data).__name__}")
        if fmt not in _SUPPORTED_FORMATS:
            raise ParseError(f"No parser for format {fmt!r}")
        parser = self._parsers[fmt]
        return parser.parse(raw_data, **kwargs)

    def scan(self, source: str | Path) -> pl.LazyFrame | None:
        """Return a lazy scan of a file-based source, or None when the format has no native scan."""
        fmt = self.detect_format(source)
        if fmt == "parquet":
            return pl.scan_parquet(source)
        if fmt == "csv":
            return pl.scan_csv(source)
        if fmt == "jsonl":
            return pl.scan_ndjson(source)
        return None
