export default function StorageLayerDoc() {
  return (
    <>
      <h1><code>StorageLayer</code></h1>
      <p><strong>File:</strong> <code>hermes/storage/__init__.py</code></p>

      <h2>What It Does</h2>
      <p>
        The <code>StorageLayer</code> composes all four storage subsystems into one
        facade. It is accessible via <code>Hermes.storage</code>.
      </p>

      <h2>Architecture</h2>
      <table>
        <thead>
          <tr><th>Component</th><th>Backend</th><th>Purpose</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><code>.cache</code> (RawCache)</td>
            <td>Parquet files on disk</td>
            <td>Cache raw API responses with TTL</td>
          </tr>
          <tr>
            <td><code>.features</code> (FeatureStore)</td>
            <td>DB table</td>
            <td>Store versioned engineered features</td>
          </tr>
          <tr>
            <td><code>.metadata</code> (MetadataRegistry)</td>
            <td>DB table</td>
            <td>Track source freshness &amp; quality</td>
          </tr>
          <tr>
            <td><code>.lineage</code> (LineageGraph)</td>
            <td>DB table</td>
            <td>Track data provenance</td>
          </tr>
        </tbody>
      </table>

      <h2>Usage</h2>
      <pre><code>{`from hermes import Hermes

hr = Hermes()

# Storage is lazy — initialized on first access
_ = hr.storage

# Cache (always available, no DB needed)
hr.storage.cache.get("fred", "get_series", "GDP", api_key)
hr.storage.cache.set("fred", "get_series", df, ttl=3600,
    "GDP", api_key)

# Feature Store, Metadata, Lineage need a DB connection
hr.storage.connect("postgresql://user:pass@localhost:5432/hermes")

hr.storage.features   # FeatureStore
hr.storage.metadata   # MetadataRegistry
hr.storage.lineage    # LineageGraph`}</code></pre>

      <h2>Cache Wiring</h2>
      <p>
        When <code>hr.storage</code> is first accessed, the <code>RawCache</code> is
        automatically assigned to all connectors (<code>fred._cache</code>,
        <code>bis._cache</code>, etc.). This enables cached connector methods:
      </p>
      <pre><code>{`hr.fred.cached_get_series("GDP", api_key)
# Uses cache automatically`}</code></pre>
    </>
  );
}
