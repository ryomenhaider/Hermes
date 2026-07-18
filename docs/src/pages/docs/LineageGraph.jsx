export default function LineageGraphDoc() {
  return (
    <>
      <h1><code>LineageGraph</code></h1>
      <p><strong>File:</strong> <code>hermes/storage/_lineage.py</code></p>

      <h2>What It Does</h2>
      <p>
        Tracks data provenance — which dataset came from which source, through which
        pipeline, with which parameters. Enables tracing any derived dataset back to
        its original raw sources.
      </p>

      <h2>Architecture</h2>
      <p>Single database table <code>_lineage</code>:</p>
      <pre><code>{`_lineage (
    dataset_id      TEXT,
    source_name     TEXT,
    pipeline_name   TEXT,
    pipeline_ver    INTEGER,
    input_params    TEXT,
    parent_id       TEXT,
    created_at      TEXT,
    PRIMARY KEY (dataset_id, source_name, created_at)
)`}</code></pre>
      <p>
        The <code>parent_id</code> field creates a linked list of provenance,
        enabling full traceability from derived features back to raw sources.
      </p>

      <h2>Methods</h2>

      <h3><code>record(dataset_id, source_name, pipeline_name="", pipeline_version=1, input_params=None, parent_id=None)</code></h3>
      <p>Record a data transformation step.</p>
      <pre><code>{`# Record raw data fetch
hr.storage.lineage.record("raw_gdp_v1", "FRED",
    pipeline_name="fred_fetch", pipeline_version=1)

# Record derived feature set (with parent)
hr.storage.lineage.record("gdp_features_v2", "FRED",
    pipeline_name="feature_engineering", pipeline_version=2,
    input_params={"window": "12m", "lag": 3},
    parent_id="raw_gdp_v1")`}</code></pre>

      <h3><code>trace(dataset_id) → list[dict]</code></h3>
      <p>Walk the parent chain to get the full provenance.</p>
      <pre><code>{`trace = hr.storage.lineage.trace("gdp_features_v2")
for t in trace:
    print(f"{t['dataset_id']} ← {t['source_name']} ({t['pipeline_name']})")`}</code></pre>

      <h3><code>sources_of(dataset_id) → list[str]</code></h3>
      <p>Get all unique source names that contributed to a dataset.</p>
      <pre><code>{`sources = hr.storage.lineage.sources_of("gdp_features_v2")
# Returns: ['FRED', 'BIS']
print(f"Data sourced from: {', '.join(sources)}")`}</code></pre>

      <h3><code>graph(dataset_id) → dict</code></h3>
      <p>Get a graph representation (nodes + edges) for visualization.</p>
      <pre><code>{`g = hr.storage.lineage.graph("gdp_features_v2")
print(g["nodes"])  # list of node dicts
print(g["edges"])  # list of {from, to} dicts`}</code></pre>

      <h2>Example Lineage Chain</h2>
      <pre><code>{`raw_gdp_v1  ←  FRED  (fred_fetch v1)
    ↓
gdp_features_v1  ←  FRED  (feature_engineering v1)
    ↓
gdp_features_v2  ←  FRED  (feature_engineering v2)
                      BIS  (bis_credit_data v1)`}</code></pre>
    </>
  );
}
