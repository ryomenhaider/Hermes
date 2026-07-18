from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import pandas as pd


CACHE_DIR = Path.home() / ".hermes" / "cache"


class RawCache:
    def __init__(self, cache_dir: str | Path | None = None):
        self._cache_dir = Path(cache_dir) if cache_dir else CACHE_DIR
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def _key(self, source: str, method: str, *args: Any, **kwargs: Any) -> str:
        raw = f"{source}:{method}:{args}:{sorted(kwargs.items())}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def _path(self, key: str) -> Path:
        return self._cache_dir / key[:2] / key[2:4] / f"{key}.parquet"

    def _meta_path(self, key: str) -> Path:
        p = self._path(key)
        return p.with_suffix(".meta.json")

    def get(self, source: str, method: str, *args: Any, **kwargs: Any) -> pd.DataFrame | None:
        key = self._key(source, method, *args, **kwargs)
        meta_path = self._meta_path(key)
        data_path = self._path(key)

        if not meta_path.exists() or not data_path.exists():
            return None

        try:
            meta = json.loads(meta_path.read_text())
            expires = datetime.fromisoformat(meta.get("expires", "1970-01-01T00:00:00+00:00"))
            if datetime.now(timezone.utc) > expires:
                self._remove(key)
                return None
            return pd.read_parquet(data_path)
        except Exception:
            self._remove(key)
            return None

    def set(
        self,
        source: str,
        method: str,
        df: pd.DataFrame,
        ttl: int = 3600,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        key = self._key(source, method, *args, **kwargs)
        data_path = self._path(key)
        meta_path = self._meta_path(key)

        data_path.parent.mkdir(parents=True, exist_ok=True)

        expires = (datetime.now(timezone.utc) + timedelta(seconds=ttl)).isoformat()
        meta = {
            "source": source,
            "method": method,
            "created": datetime.now(timezone.utc).isoformat(),
            "expires": expires,
            "ttl": ttl,
            "rows": len(df),
            "columns": list(df.columns),
        }
        meta_path.write_text(json.dumps(meta, indent=2))
        df.to_parquet(data_path, index=False)

    def invalidate(self, source: str | None = None, method: str | None = None) -> int:
        count = 0
        for meta_file in self._cache_dir.rglob("*.meta.json"):
            try:
                meta = json.loads(meta_file.read_text())
                if source and meta.get("source") != source:
                    continue
                if method and meta.get("method") != method:
                    continue
                key = meta_file.stem
                self._remove(key)
                count += 1
            except Exception:
                pass
        return count

    def clear(self, older_than: timedelta | None = None) -> int:
        if older_than is None:
            count = 0
            for f in self._cache_dir.rglob("*"):
                if f.is_file():
                    f.unlink()
                    count += 1
            for d in self._cache_dir.rglob("*"):
                if d.is_dir() and not any(d.iterdir()):
                    d.rmdir()
            return count

        count = 0
        cutoff = datetime.now(timezone.utc) - older_than
        for meta_file in self._cache_dir.rglob("*.meta.json"):
            try:
                mtime = datetime.fromtimestamp(meta_file.stat().st_mtime, tz=timezone.utc)
                if mtime < cutoff:
                    key = meta_file.stem
                    self._remove(key)
                    count += 1
            except Exception:
                pass
        return count

    def _remove(self, key: str) -> None:
        data_path = self._path(key)
        meta_path = self._meta_path(key)
        data_path.unlink(missing_ok=True)
        meta_path.unlink(missing_ok=True)
        parent = data_path.parent
        while parent != self._cache_dir:
            if parent.exists() and not any(parent.iterdir()):
                parent.rmdir()
            parent = parent.parent

    def cached(self, ttl: int = 3600) -> Callable:
        def decorator(fn: Callable) -> Callable:
            def wrapper(source_name: str, *args: Any, **kwargs: Any) -> pd.DataFrame:
                cached = self.get(source_name, fn.__name__, *args, **kwargs)
                if cached is not None:
                    return cached
                result = fn(*args, **kwargs)
                if isinstance(result, pd.DataFrame):
                    self.set(source_name, fn.__name__, result, ttl, *args, **kwargs)
                return result
            wrapper.__name__ = fn.__name__
            wrapper.__doc__ = fn.__doc__
            return wrapper
        return decorator
