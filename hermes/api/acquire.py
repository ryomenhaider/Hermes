from __future__ import annotations

from pathlib import Path

from hermes.api.data import parse as _parse
from hermes.connectors import (
    Binance,
    FINNHUB,
    FRED,
    IMF,
    OpenSanction,
    SECEDGAR,
    World_bank,
    Yfinance,
)
from hermes.core.dataset import Dataset
from hermes.core.errors import AcquisitionError, ConnectorNotFoundError

# Connector sources with a fetch()-style interface. GDELT and the bundled
# public_data datasets are excluded: GDELT is roadmap-gated, public_data is a
# local file bundle (use hr.read(path) / hr.ingest(path) for it).
_CONNECTORS = {
    "binance": Binance,
    "finnhub": FINNHUB,
    "fred": FRED,
    "imf": IMF,
    "opensanctions": OpenSanction,
    "sec": SECEDGAR,
    "world_bank": World_bank,
    "yfinance": Yfinance,
}


def _connector(source: str):
    key = str(source).strip().lower()
    try:
        cls = _CONNECTORS[key]
    except KeyError:
        raise ConnectorNotFoundError(
            f"Unknown source {source!r}. Known sources: {sorted(_CONNECTORS)}"
        ) from None
    return cls()


def fetch(source: str, **kwargs):
    """Run an API source through its connector (cached, parsed, validated)."""
    return _connector(source).fetch(**kwargs)


def fetch_raw(source: str, **kwargs):
    """Raw source response; bypasses the connector cache/parse/Dataset wrapping."""
    return _connector(source)._fetch(**kwargs)  # noqa: SLF001 - the public raw-fetch contract


def read(path: str | Path, format: str | None = None, **kwargs) -> Dataset:
    """Parse a local file into a Dataset (file source)."""
    return _parse(path, format=format, **kwargs)


def ingest(source: str | Path, **kwargs) -> Dataset:
    """Acquire a Dataset from an API source name or a file path."""
    if isinstance(source, (str, Path)) and Path(str(source)).exists():
        return read(source, format=kwargs.pop("format", None), **kwargs)

    result = fetch(source, **kwargs)
    if isinstance(result, Dataset):
        return result
    if result is None:
        raise AcquisitionError(f"Source {source!r} returned no data")
    return _parse(result)


def sync(source: str, **kwargs) -> Dataset:
    """Refresh a source through its cache and return the current Dataset."""
    kwargs.setdefault("force", True)
    return ingest(source, **kwargs)
    # ponytail: full refetch, not cursor-based incremental sync; sync state is deferred (spec E2)


__all__ = ["fetch", "fetch_raw", "ingest", "read", "sync"]