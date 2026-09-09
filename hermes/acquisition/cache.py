import hashlib
import json
import logging
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta
from pathlib import Path

import polars as pl

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = Path.home() / ".hermes_cache" / "raw"

DEFAULT_TTL = timedelta(hours=24)


class CacheMiss(Exception):
    pass


class RawCache:
    def __init__(self, cache_dir: str | Path | None = None):
        self.cache_dir = Path(cache_dir) if cache_dir else DEFAULT_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._hits: dict[str, int] = {}
        self._misses: dict[str, int] = {}

    def _source_dir(self, source: str) -> Path:
        p = self.cache_dir / source
        p.mkdir(parents=True, exist_ok=True)
        return p

    def _key_path(self, source: str, params: dict) -> Path:
        raw = f"{source}:{json.dumps(params, sort_keys=True, default=str)}"
        h = hashlib.sha256(raw.encode()).hexdigest()[:16]
        return self._source_dir(source) / f"{h}.parquet"

    def get(self, source: str, params: dict, ttl: timedelta | None = None) -> pl.DataFrame:
        path = self._key_path(source, params)
        if not path.exists():
            self._misses[source] = self._misses.get(source, 0) + 1
            raise CacheMiss(f"No cache for {source}:{params}")

        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        ttl = ttl or DEFAULT_TTL
        age = datetime.now() - mtime

        if age > ttl:
            path.unlink(missing_ok=True)
            meta = path.with_suffix(".meta.json")
            meta.unlink(missing_ok=True)
            self._misses[source] = self._misses.get(source, 0) + 1
            raise CacheMiss(f"Cache expired for {source}:{params} (age={age})")

        try:
            df = pl.read_parquet(path)
        except Exception as e:
            logger.warning(f"Corrupted cache file {path}: {e}")
            path.unlink(missing_ok=True)
            self._misses[source] = self._misses.get(source, 0) + 1
            raise CacheMiss(f"Corrupted cache for {source}:{params}") from e

        self._hits[source] = self._hits.get(source, 0) + 1
        logger.debug(f"Cache HIT for {source}:{params}")
        return df

    def put(self, source: str, params: dict, df: pl.DataFrame):
        path = self._key_path(source, params)
        df.write_parquet(path)
        meta = {
            "source": source,
            "params": params,
            "cached_at": datetime.now().isoformat(),
            "rows": df.height,
            "columns": df.columns,
        }
        meta_path = path.with_suffix(".meta.json")
        meta_path.write_text(json.dumps(meta, indent=2, default=str))
        logger.debug(f"Cached {df.height} rows for {source}:{params}")

    async def get_or_fetch(
        self,
        source: str,
        params: dict,
        fetch_fn: Callable[[], Awaitable[pl.DataFrame]],
        force: bool = False,
        ttl: timedelta | None = None,
    ) -> pl.DataFrame:
        if not force:
            try:
                return self.get(source, params, ttl=ttl)
            except CacheMiss:
                pass

        df = await fetch_fn()
        if isinstance(df, pl.DataFrame) and not df.is_empty():
            self.put(source, params, df)
        return df

    def clear(self, older_than: timedelta | None = None):
        now = datetime.now()
        removed = 0
        for p in self.cache_dir.rglob("*.parquet"):
            age = now - datetime.fromtimestamp(p.stat().st_mtime)
            if older_than is None or age > older_than:
                p.unlink(missing_ok=True)
                meta = p.with_suffix(".meta.json")
                meta.unlink(missing_ok=True)
                removed += 1
        logger.info(f"Cleared {removed} cache files")

    def stats(self) -> dict:
        total = 0
        by_source: dict[str, int] = {}
        for p in self.cache_dir.rglob("*.parquet"):
            total += 1
            source = p.parent.name
            by_source[source] = by_source.get(source, 0) + 1
        hit_rate = {}
        for src in set(list(self._hits.keys()) + list(self._misses.keys())):
            h = self._hits.get(src, 0)
            m = self._misses.get(src, 0)
            total_calls = h + m
            hit_rate[src] = round(h / total_calls, 4) if total_calls > 0 else 0
        return {
            "total_files": total,
            "by_source": by_source,
            "hits": dict(self._hits),
            "misses": dict(self._misses),
            "hit_rate": hit_rate,
        }
