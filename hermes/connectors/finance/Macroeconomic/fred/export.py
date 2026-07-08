import logging
from typing import Any

logger = logging.getLogger(__name__)


class FredExporter:

    def export(
        self,
        data: list[dict[str, Any]],
        destination: str,
        format: str = "json",
    ) -> None:
        ...
