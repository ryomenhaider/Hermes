export default function RawCacheDoc() {
  return (
    <>
      <h1><code>RawCache</code></h1>
      <p><strong>File:</strong> <code>hermes/storage/_cache.py</code></p>

      <h2>What It Does</h2>
      <p>
        Stores raw API responses as Parquet files on disk with TTL-based expiration.
        Cache keys are SHA-256 hashes of <code>(source, method, *args, **kwargs)</code>.
        Each cached entry gets a <code>.meta.json</code> sidecar file tracking source,
        TTL, row count, and columns.
      </p>

      <h2>Architecture</h2>
      <p>Cache directory structure:</p>
      <pre><code>{`~/.hermes/cache/
  ab/
    cd/
      abcdef123456...sha256.parquet
      abcdef123456...sha256.meta.json
  ef/
    ...`}</code></pre>
      <p>
        Files are sharded by the first 4 hex characters of the key to avoid any single
        directory having too many entries.
      </p>

      <h2>Methods</h2>

      <h3><code>get(source, method, *args, **kwargs) → DataFrame | None</code></h3>
      <p>Returns cached data if it exists and hasn't expired. <code>None</code> on cache miss.</p>
      <pre><code>{`cache.get("fred", "get_series", "GDP", api_key)
# Returns DataFrame or None`}</code></pre>

      <h3><code>set(source, method, df, ttl=3600, *args, **kwargs)</code></h3>
      <p>Cache a DataFrame with a TTL in seconds (default 1 hour).</p>
      <pre><code>{`cache.set("fred", "get_series", df, ttl=3600, "GDP", api_key)`}</code></pre>

      <h3><code>invalidate(source=None, method=None) → int</code></h3>
      <p>Remove cached entries. Filter by source and/or method.</p>
      <pre><code>{`cache.invalidate()              # clear everything
cache.invalidate(source="fred")  # clear all FRED cache
cache.invalidate(source="fred", method="get_series")`}</code></pre>

      <h3><code>clear(older_than=None) → int</code></h3>
      <p>Remove entries older than a timedelta. If no argument, clears all.</p>
      <pre><code>{`from datetime import timedelta
cache.clear(older_than=timedelta(days=7))
cache.clear()  # clear everything`}</code></pre>

      <h3><code>cached(ttl=3600) → Callable</code></h3>
      <p>Decorator that wraps any function with cache get/set logic.</p>
      <pre><code>{`@cache.cached(ttl=3600)
def expensive_query(source, param):
    # ... API call ...
    return df`}</code></pre>
    </>
  );
}
