from __future__ import annotations

import time
from datetime import timedelta

import polars as pl
import pytest
from polars.testing import assert_frame_equal

from hermes.acquisition.cache import CacheMiss, RawCache


class TestRawCache:
    def test_init_creates_dir(self, tmp_cache: RawCache):
        assert tmp_cache.cache_dir.exists()

    def test_put_and_get(self, tmp_cache: RawCache):
        df = pl.DataFrame({"a": [1, 2, 3]})
        tmp_cache.put("test_source", {"key": "val"}, df)
        result = tmp_cache.get("test_source", {"key": "val"})
        assert_frame_equal(result, df)

    def test_get_miss(self, tmp_cache: RawCache):
        with pytest.raises(CacheMiss):
            tmp_cache.get("no_source", {"k": "v"})

    def test_get_expired(self, tmp_cache: RawCache):
        df = pl.DataFrame({"a": [1]})
        tmp_cache.put("src", {"k": "v"}, df)
        import time as _time

        _time.sleep(0.015)
        with pytest.raises(CacheMiss):
            tmp_cache.get("src", {"k": "v"}, ttl=timedelta(milliseconds=5))

    def test_get_corrupted(self, tmp_cache: RawCache):
        path = tmp_cache._key_path("src", {"k": "v"})
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"not a parquet file")
        with pytest.raises(CacheMiss):
            tmp_cache.get("src", {"k": "v"})

    async def test_get_or_fetch_hit(self, tmp_cache: RawCache):
        tmp_cache.put("src", {"k": "v"}, pl.DataFrame({"x": [1]}))
        called = False

        async def fetch():
            nonlocal called
            called = True
            return pl.DataFrame({"x": [2]})

        result = await tmp_cache.get_or_fetch("src", {"k": "v"}, fetch)
        assert called is False
        assert result["x"].item(0) == 1

    async def test_get_or_fetch_miss(self, tmp_cache: RawCache):
        called = False

        async def fetch():
            nonlocal called
            called = True
            return pl.DataFrame({"x": [42]})

        result = await tmp_cache.get_or_fetch("src", {"k": "v"}, fetch)
        assert called
        assert result["x"].item(0) == 42

    async def test_get_or_fetch_force(self, tmp_cache: RawCache):
        tmp_cache.put("src", {"k": "v"}, pl.DataFrame({"x": [1]}))
        called = False

        async def fetch():
            nonlocal called
            called = True
            return pl.DataFrame({"x": [99]})

        result = await tmp_cache.get_or_fetch("src", {"k": "v"}, fetch, force=True)
        assert called
        assert result["x"].item(0) == 99

    async def test_get_or_fetch_empty_df_not_cached(self, tmp_cache: RawCache):
        called = False

        async def fetch():
            nonlocal called
            called = True
            return pl.DataFrame()

        result = await tmp_cache.get_or_fetch("src", {"k": "v"}, fetch)
        assert called
        assert result.is_empty()
        with pytest.raises(CacheMiss):
            tmp_cache.get("src", {"k": "v"})

    def test_clear_all(self, tmp_cache: RawCache):
        tmp_cache.put("s1", {"k": "v"}, pl.DataFrame({"a": [1]}))
        tmp_cache.put("s2", {"k": "v"}, pl.DataFrame({"b": [2]}))
        tmp_cache.clear()
        assert len(list(tmp_cache.cache_dir.rglob("*.parquet"))) == 0

    def test_clear_older_than(self, tmp_cache: RawCache):
        tmp_cache.put("s1", {"k": "v"}, pl.DataFrame({"a": [1]}))
        time.sleep(0.01)
        tmp_cache.clear(older_than=timedelta(milliseconds=5))
        assert len(list(tmp_cache.cache_dir.rglob("*.parquet"))) == 0

    def test_stats_empty(self, tmp_cache: RawCache):
        stats = tmp_cache.stats()
        assert stats["total_files"] == 0
        assert stats["hits"] == {}
        assert stats["misses"] == {}

    def test_stats_with_hits_and_misses(self, tmp_cache: RawCache):
        tmp_cache.put("s1", {"k": "v"}, pl.DataFrame({"a": [1]}))
        tmp_cache.get("s1", {"k": "v"})
        with pytest.raises(CacheMiss):
            tmp_cache.get("s1", {"k2": "v2"})
        stats = tmp_cache.stats()
        assert stats["total_files"] == 1
        assert stats["hits"]["s1"] == 1
        assert stats["misses"]["s1"] == 1
        assert stats["hit_rate"]["s1"] == 0.5

    def test_key_path_deterministic(self, tmp_cache: RawCache):
        p1 = tmp_cache._key_path("src", {"a": 1, "b": 2})
        p2 = tmp_cache._key_path("src", {"b": 2, "a": 1})
        assert p1 == p2

    def test_meta_json_written(self, tmp_cache: RawCache):
        df = pl.DataFrame({"x": [1]})
        tmp_cache.put("src", {"p": "v"}, df)
        path = tmp_cache._key_path("src", {"p": "v"})
        meta = path.with_suffix(".meta.json")
        assert meta.exists()
        import json

        data = json.loads(meta.read_text())
        assert data["source"] == "src"
        assert data["rows"] == 1
