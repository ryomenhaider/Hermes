from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_CACHE_DIR = Path.home() / ".hermes_cache"


class DataCache:
    def __init__(self, cache_dir: str | Path | None = None):
        self._dir = Path(cache_dir) if cache_dir else DEFAULT_CACHE_DIR
        self._dir.mkdir(parents=True, exist_ok=True)

    def _key(self, *args: Any, **kwargs: Any) -> str:
        raw = f"{args}:{sorted(kwargs.items())}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def _data_path(self, key: str) -> Path:
        return self._dir / key[:2] / key[2:4] / f"{key}.parquet"

    def _meta_path(self, key: str) -> Path:
        return self._data_path(key).with_suffix(".meta.json")

    def get(self, *args: Any, **kwargs: Any) -> pd.DataFrame | None:
        key = self._key(*args, **kwargs)
        dp = self._data_path(key)
        mp = self._meta_path(key)
        if not dp.exists() or not mp.exists():
            return None
        try:
            meta = json.loads(mp.read_text())
            expires = datetime.fromisoformat(meta.get("expires", ""))
            if datetime.now(timezone.utc) > expires:
                dp.unlink(missing_ok=True)
                mp.unlink(missing_ok=True)
                return None
            return pd.read_parquet(dp)
        except Exception:
            return None

    def set(self, df: pd.DataFrame, ttl: int = 3600, *args: Any, **kwargs: Any) -> None:
        key = self._key(*args, **kwargs)
        dp = self._data_path(key)
        mp = self._meta_path(key)
        dp.parent.mkdir(parents=True, exist_ok=True)
        expires = (datetime.now(timezone.utc) + timedelta(seconds=ttl)).isoformat()
        mp.write_text(json.dumps({"expires": expires, "rows": len(df)}))
        df.to_parquet(dp, index=False)
