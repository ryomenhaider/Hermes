export default function FredDoc() {
  return (
    <>
      <h1><code>Fred</code> Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/fred.py</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches economic time series from the Federal Reserve Economic Data (FRED) API.
        FRED provides US and international macro data: GDP, unemployment, CPI, interest rates,
        stock market indices, and thousands more.
      </p>
      <p><strong>Authentication:</strong> Free API key (any email) at <a href="https://fred.stlouisfed.org/docs/api/api_key.html" target="_blank">fred.stlouisfed.org</a>.</p>

      <h2>Architecture</h2>
      <p>The connector follows a two-class pattern:</p>
      <ul>
        <li><strong><code>FredLogic</code></strong> — Stateless logic class with fetch, validate, transform, and export methods. All HTTP calls go through <code>httpx</code>.</li>
        <li><strong><code>Fred</code></strong> — Stateful user-facing class that composes <code>FredLogic</code>, stores the API key, and provides cached variants.</li>
      </ul>

      <h2>Methods</h2>

      <h3><code>connect(api_key: str) → str</code></h3>
      <p>Store the FRED API key for subsequent calls.</p>
      <pre><code>{`hr.fred.connect("abc123...")`}</code></pre>

      <h3><code>get_series(series_id, api=None, export=None, filetype=None) → DataFrame</code></h3>
      <p>Fetch observations for a FRED series. Returns a canonical DataFrame with columns: <code>date</code>, <code>country_iso3</code>, <code>indicator_id</code>, <code>value</code>, <code>source</code>.</p>
      <pre><code>{`gdp = hr.fred.get_series("GDP", api_key)
# Returns: DataFrame with US GDP data

gdp = hr.fred.get_series("GDP", api_key,
    export=True, filetype="parquet")
# Also exports to data/fred{timestamp}.parquet`}</code></pre>

      <h3><code>cached_get_series(series_id, api=None, ttl=3600) → DataFrame</code></h3>
      <p>Same as <code>get_series</code> but checks the Parquet cache first. Only works if the storage layer has been initialized (i.e., <code>hr.storage</code> was accessed).</p>
      <pre><code>{`_ = hr.storage  # initialize cache wiring
gdp = hr.fred.cached_get_series("GDP", api_key)
# First call: hits API, caches result
# Subsequent calls: reads from ~/.hermes/cache/`}</code></pre>

      <h3><code>get_series_metadata(series_id, api=None, export=None, filetype=None, normalize=True) → DataFrame</code></h3>
      <p>Fetch metadata about a series (title, frequency, units, notes, etc.).</p>
      <pre><code>{`meta = hr.fred.get_series_metadata("GDP", api_key)
# Returns: DataFrame with series metadata`}</code></pre>

      <h3><code>search_series(query, limit=25, api=None) → DataFrame</code></h3>
      <p>Search FRED for series matching a text query.</p>
      <pre><code>{`results = hr.fred.search_series("inflation", limit=10)`}</code></pre>

      <h3><code>get_multiple_series(series_ids, api=None, export=None, filetype=None, normalize=True) → DataFrame</code></h3>
      <p>Fetch multiple series at once and combine into a single DataFrame.</p>
      <pre><code>{`df = hr.fred.get_multiple_series(["GDP", "UNRATE"], api_key)`}</code></pre>

      <h3><code>get_categories(api=None) → DataFrame</code></h3>
      <p>List FRED categories.</p>

      <h3><code>get_series_in_category(category_id, limit=100, api=None) → DataFrame</code></h3>
      <p>List all series in a FRED category.</p>

      <h3><code>list_common_series() → dict</code></h3>
      <p>Return a dictionary of commonly used series IDs.</p>
      <pre><code>{`print(Fred.list_common_series())
# {'GDP': 'GDP', 'UNEMPLOYMENT': 'UNRATE', 'CPI': 'CPIAUCSL', ...}`}</code></pre>
    </>
  );
}
