export default function WorldBankDoc() {
  return (
    <>
      <h1><code>World_Bank</code> Connector</h1>
      <p><strong>File:</strong> <code>hermes/sources/world_bank.py</code></p>

      <h2>What It Does</h2>
      <p>
        Fetches global development indicators from the World Bank API.
        Covers 3000+ indicators across GDP, poverty, governance, education, health,
        infrastructure, and more. No authentication required.
      </p>
      <p><strong>API:</strong> <a href="https://data.worldbank.org/" target="_blank">data.worldbank.org</a></p>

      <h2>Architecture</h2>
      <ul>
        <li><strong><code>WBLogic</code></strong> — Handles World Bank API v2 requests, response parsing, validation, and canonical transformation.</li>
        <li><strong><code>World_Bank</code></strong> — User-facing class.</li>
      </ul>

      <h2>Methods</h2>

      <h3><code>get_indicator(indicator, country=None, date_range=None, ...) → DataFrame</code></h3>
      <p>Fetch a World Bank indicator for one or more countries. Returns canonical DataFrame.</p>
      <pre><code>{`# GDP per capita for China
df = hr.world_bank.get_indicator("NY.GDP.PCAP.CD",
    country="CHN")

# Multiple countries
df = hr.world_bank.get_indicator("NY.GDP.MKTP.CD",
    country=["USA", "CHN", "JPN", "DEU"])

# With date range
df = hr.world_bank.get_indicator("SL.UEM.TOTL.ZS",
    country="USA",
    date_range=("2010", "2024"))`}</code></pre>

      <h3><code>get_indicator_metadata(indicator) → dict</code></h3>
      <p>Fetch metadata about a specific indicator.</p>
      <pre><code>{`meta = hr.world_bank.get_indicator_metadata("NY.GDP.PCAP.CD")
print(meta["name"])
# "GDP per capita (current US$)"`}</code></pre>

      <h3><code>export(data, filetype) → str</code></h3>
      <p>Export to CSV, JSON, Parquet, or Pickle.</p>
    </>
  );
}
