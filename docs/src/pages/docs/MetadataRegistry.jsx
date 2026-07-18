export default function MetadataRegistryDoc() {
  return (
    <>
      <h1><code>MetadataRegistry</code></h1>
      <p><strong>File:</strong> <code>hermes/storage/_metadata.py</code></p>

      <h2>What It Does</h2>
      <p>
        Tracks per-connector metadata: when data was last fetched, how many rows,
        quality scores, and checksums. Powers freshness checks and staleness reports.
      </p>

      <h2>Architecture</h2>
      <p>Single database table <code>_source_registry</code>:</p>
      <pre><code>{`_source_registry (
    source_name   TEXT,
    indicator_id  TEXT,
    last_fetched  TEXT,
    row_count     INTEGER,
    quality_score REAL,
    checksum      TEXT,
    schema_ver    INTEGER,
    PRIMARY KEY (source_name, indicator_id)
)`}</code></pre>

      <h2>Methods</h2>

      <h3><code>register(source, indicator, row_count=0, quality_score=0.0, checksum="")</code></h3>
      <p>Register or update a source-indicator pair.</p>
      <pre><code>{`hr.storage.metadata.register("FRED", "GDP",
    row_count=1000, quality_score=0.95,
    checksum="sha256abc...")`}</code></pre>

      <h3><code>update(source, indicator, **fields)</code></h3>
      <p>Update specific fields for a registered source.</p>
      <pre><code>{`hr.storage.metadata.update("FRED", "GDP",
    row_count=1500)`}</code></pre>

      <h3><code>get(source, indicator) → MetadataRecord | None</code></h3>
      <p>Get the metadata record for a source-indicator pair.</p>
      <pre><code>{`record = hr.storage.metadata.get("FRED", "GDP")
if record:
    print(f"Last fetched: {record.last_fetched}")
    print(f"Quality: {record.quality_score}")`}</code></pre>

      <h3><code>list(include_quality=False) → list[dict]</code></h3>
      <p>List all registered sources.</p>
      <pre><code>{`sources = hr.storage.metadata.list(include_quality=True)
for s in sources:
    print(f"{s['source']} - {s['indicator']}: {s['quality_score']}")`}</code></pre>

      <h3><code>check_freshness(source, indicator, max_age_hours=24) → bool</code></h3>
      <p>Check if data was fetched within the max age window.</p>
      <pre><code>{`if not hr.storage.metadata.check_freshness("FRED", "GDP"):
    # Data is stale, re-fetch
    gdp = hr.fred.get_series("GDP", api_key)`}</code></pre>

      <h3><code>staleness_report() → list[dict]</code></h3>
      <p>Get a full freshness report for all tracked sources.</p>
      <pre><code>{`report = hr.storage.metadata.staleness_report()
for r in report:
    print(f"{r['source']}/{r['indicator']}: {r['age_hours']}h old")`}</code></pre>
    </>
  );
}
