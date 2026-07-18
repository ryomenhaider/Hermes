export default function FeatureStoreDoc() {
  return (
    <>
      <h1><code>FeatureStore</code></h1>
      <p><strong>File:</strong> <code>hermes/storage/_feature_store.py</code></p>

      <h2>What It Does</h2>
      <p>
        Stores engineered feature DataFrames in database tables with versioning.
        Each feature set gets its own table (<code>features_{name}</code>) with
        auto-created columns matching the DataFrame schema.
      </p>

      <h2>Architecture</h2>
      <ul>
        <li>Feature set tables are created dynamically based on DataFrame dtypes</li>
        <li>A <code>_version</code> column is added for versioning (part of the primary key)</li>
        <li>A <code>_created_at</code> column tracks when stored</li>
        <li>Registry table <code>_feature_sets</code> tracks all feature sets and their latest version</li>
      </ul>

      <h2>Methods</h2>

      <h3><code>store(df, feature_set, version=None, description="") → int</code></h3>
      <p>Store a DataFrame as a versioned feature set. Returns the version number.</p>
      <pre><code>{`# Manual version
fs.store(df, "gdp_features", version=1)

# Auto-increment version
v = fs.store(df, "gdp_features")
print(f"Stored as version {v}")
# If version 1 exists, this stores as version 2`}</code></pre>

      <h3><code>load(feature_set, version=None, filters=None) → DataFrame</code></h3>
      <p>Load a feature set, optionally filtering by version and/or field values.</p>
      <pre><code>{`# Load latest version
df = fs.load("gdp_features")

# Load specific version
df = fs.load("gdp_features", version=1)

# Load with filters
df = fs.load("gdp_features",
    version=1,
    filters={"country_iso3": "USA"})`}</code></pre>

      <h3><code>list_feature_sets() → list[dict]</code></h3>
      <p>List all stored feature sets with name, latest version, and description.</p>
      <pre><code>{`for fs_info in fs.list_feature_sets():
    print(f"{fs_info['name']} v{fs_info['latest_version']}")`}</code></pre>

      <h3><code>delete(feature_set, version=None) → int</code></h3>
      <p>Delete a specific version or the entire feature set.</p>
      <pre><code>{`fs.delete("gdp_features", version=1)  # remove v1 only
fs.delete("gdp_features")             # drop entire table`}</code></pre>

      <h2>DataFrame to SQL Type Mapping</h2>
      <table>
        <thead>
          <tr><th>pandas dtype</th><th>SQL type</th></tr>
        </thead>
        <tbody>
          <tr><td><code>int64</code></td><td><code>BIGINT</code></td></tr>
          <tr><td><code>float64</code></td><td><code>DOUBLE PRECISION</code></td></tr>
          <tr><td><code>object</code> / <code>string</code></td><td><code>TEXT</code></td></tr>
          <tr><td><code>bool</code></td><td><code>BOOLEAN</code></td></tr>
          <tr><td><code>datetime64[ns]</code></td><td><code>TIMESTAMPTZ</code></td></tr>
          <tr><td><code>category</code></td><td><code>TEXT</code></td></tr>
        </tbody>
      </table>
    </>
  );
}
