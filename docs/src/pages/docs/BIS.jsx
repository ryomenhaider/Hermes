export default function BISDoc() {
  return (
    <>
      <h1><code>BIS</code> Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/bis.py</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches banking, credit, exchange rate, and property price statistics from the
        Bank for International Settlements (BIS) API. No authentication required.
      </p>
      <p><strong>API:</strong> <a href="https://stats.bis.org/api-doc/" target="_blank">stats.bis.org</a></p>

      <h2>Architecture</h2>
      <p>Two-class pattern:</p>
      <ul>
        <li><strong><code>BISLogic</code></strong> — Handles SDMX protocol: auto-discovers dimension order from <code>serieskeysonly</code> CSV responses, builds SDMX keys, normalises countries to ISO3 via <code>pycountry</code>.</li>
        <li><strong><code>BIS</code></strong> — User-facing class with cache wiring support and export methods.</li>
      </ul>

      <h2>Methods</h2>

      <h3><code>get_flows() → DataFrame</code></h3>
      <p>List all available BIS data flows.</p>
      <pre><code>{`flows = hr.bis.get_flows()
print(flows)
#       id                description
#  WS_EER  Effective exchange rates
# WS_...   ...`}</code></pre>

      <h3><code>get_dimensions(flow: str) → DataFrame</code></h3>
      <p>List dimensions (columns) for a specific data flow.</p>
      <pre><code>{`dims = hr.bis.get_dimensions("WS_EER")
print(dims)
# ['FREQ', 'REF_AREA', 'EER_TYPE', ...]`}</code></pre>

      <h3><code>get_data(flow, filters=None, key=None, ...) → DataFrame</code></h3>
      <p>Fetch data for a BIS flow with optional filters. Returns canonical DataFrame.</p>
      <pre><code>{`# Filter-based
df = hr.bis.get_data("WS_EER",
    filters={"FREQ": "M", "EER_TYPE": "N", "REF_AREA": "JP"})

# Key-based (SDMX key, '.' = wildcard)
df = hr.bis.get_data("WS_CBPOL", key="M.US")

# With export
df = hr.bis.get_data("WS_EER",
    filters={"FREQ": "M", "REF_AREA": "JP"},
    export=True, filetype="csv")`}</code></pre>
      <p>The BIS connector auto-normalises countries using <code>pycountry</code> (ISO2 to ISO3),
      with a special override for Kosovo (<code>XK</code> → <code>XKX</code>).</p>

      <h3><code>explore(flow, max_dim_values=20) → dict</code></h3>
      <p>Explore available dimension values for a flow. Returns a dict keyed by dimension name.</p>
      <pre><code>{`explore = hr.bis.explore("WS_EER")
print(explore.keys())
# dict_keys(['FREQ', 'REF_AREA', 'EER_TYPE', ...])
print(explore['FREQ'])
# {'M': 'Monthly', 'Q': 'Quarterly', ...}`}</code></pre>

      <h3><code>validate(data) → bool</code></h3>
      <p>Validate that a fetched DataFrame conforms to the canonical schema.</p>

      <h3><code>export(data, filetype) → str</code></h3>
      <p>Export a DataFrame to CSV, JSON, Parquet, or Pickle.</p>
    </>
  );
}
