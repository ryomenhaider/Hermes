export default function IMFDoc() {
  return (
    <>
      <h1><code>IMF</code> Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/imf.py</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches financial statistics from the International Monetary Fund (IMF) API.
        Covers International Financial Statistics (IFS), Balance of Payments (BOP),
        World Economic Outlook (WEO), and Government Finance Statistics (GFS).
        No authentication required.
      </p>
      <p><strong>API:</strong> <a href="https://data.imf.org/" target="_blank">data.imf.org</a></p>

      <h2>Architecture</h2>
      <ul>
        <li><strong><code>IMFLogic</code></strong> — Handles the JSON-stat format used by IMF's SDMX-JSON API. Parses dimension metadata, builds queries, and transforms responses.</li>
        <li><strong><code>IMF</code></strong> — User-facing class that composes <code>IMFLogic</code>.</li>
      </ul>

      <h2>Methods</h2>

      <h3><code>get_data(flow, country=None, indicator=None, freq=None, start=None, end=None, ...) → DataFrame</code></h3>
      <p>Fetch data from an IMF data flow. Returns canonical DataFrame.</p>
      <pre><code>{`# IFS — GDP in national currency
df = hr.imf.get_data("IFS",
    country="US",
    indicator="NGDP_XDC",
    freq="A")

# WEO — Gross domestic product, constant prices
df = hr.imf.get_data("WEO",
    country="CHN",
    indicator="NGDP_RPCH",
    freq="A")`}</code></pre>

      <h3><code>export(data, filetype) → str</code></h3>
      <p>Export DataFrame to CSV, JSON, Parquet, or Pickle.</p>
    </>
  );
}
