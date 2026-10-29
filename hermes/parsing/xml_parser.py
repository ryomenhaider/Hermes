from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import polars as pl
except ImportError:
    print("This Module Need Polars and PyArrow Installed, use pip/uv install/add hermes-plt[data] ")

from hermes.core.errors import ParseError


class XMLParser:
    def parse(self, raw_data: object, **kwargs: object) -> pl.DataFrame:
        try:
            content: str
            if isinstance(raw_data, Path):
                content = raw_data.read_text(errors="replace")
            elif isinstance(raw_data, (bytes, bytearray)):
                content = bytes(raw_data).decode(errors="replace")
            else:
                content = str(raw_data)

            root = ET.fromstring(content)
            children = list(root)
            if children and all(len(child) == 0 for child in children):
                records = [root]
            else:
                records = children or [root]

            rows = [row for row in (dict(self._flatten(record)) for record in records) if row]
            return pl.DataFrame(rows)
        except ParseError:
            raise
        except Exception as exc:
            raise ParseError(f"Failed to parse XML: {exc}") from exc

    @staticmethod
    def _flatten(elem: ET.Element, prefix: str = ""):
        for child in elem:
            key = f"{prefix}{child.tag.split('}')[-1]}"
            if list(child):
                yield from XMLParser._flatten(child, key + ".")
            else:
                yield key, child.text
