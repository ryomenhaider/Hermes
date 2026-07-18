export default function SchemasDoc() {
  return (
    <>
      <h1>Canonical Schemas</h1>
      <p><strong>File:</strong> <code>hermes/core/schemas.py</code></p>

      <h2>What They Do</h2>
      <p>
        All Hermes connectors normalise raw API responses into canonical pandas DataFrames.
        This guarantees that any downstream consumer (Aegis, Atlas, or custom scripts)
        receives predictable column names, types, and formats regardless of the source.
      </p>

      <h2>Rules</h2>
      <ul>
        <li><code>date</code> is always <code>datetime64[ns]</code></li>
        <li><code>country_iso3</code> is always ISO 3166-1 alpha-3 uppercase</li>
        <li>Every DataFrame gets a <code>source</code> column with the connector name</li>
        <li>Connectors implement <code>_to_canonical()</code> or use <code>normalize=True/False</code></li>
      </ul>

      <h2>Seven Canonical Schemas</h2>

      <table>
        <thead>
          <tr><th>Schema</th><th>Columns</th><th>Sources</th></tr>
        </thead>
        <tbody>
          <tr>
            <td><code>indicator</code></td>
            <td><code>date, country_iso3, indicator_id, value, source</code></td>
            <td>FRED, World Bank, IMF, BIS, OECD, Eurostat, FAO, EIA, IEA, USGS</td>
          </tr>
          <tr>
            <td><code>event</code></td>
            <td><code>event_id, date, country_iso3, event_type, severity, lat, lon, source</code></td>
            <td>GDELT, UCDP, EM-DAT, PRIO</td>
          </tr>
          <tr>
            <td><code>cross_section</code></td>
            <td><code>country_iso3, year, indicator_id, value, source</code></td>
            <td>V-DEM, Freedom House, Transparency Int., SIPRI</td>
          </tr>
          <tr>
            <td><code>trade</code></td>
            <td><code>date, origin_iso3, destination_iso3, commodity_code, value, source</code></td>
            <td>UN Comtrade</td>
          </tr>
          <tr>
            <td><code>media</code></td>
            <td><code>article_id, date, source_name, title, content, sentiment, url, lang</code></td>
            <td>NewsAPI, GDELT GKG</td>
          </tr>
          <tr>
            <td><code>geospatial</code></td>
            <td><code>feature_id, feature_type, country_iso3, geometry, properties, source</code></td>
            <td>OpenStreetMap, Natural Earth</td>
          </tr>
          <tr>
            <td><code>knowledge</code></td>
            <td><code>entity_id, entity_type, label, aliases, properties, source</code></td>
            <td>Wikidata, Wikipedia API</td>
          </tr>
        </tbody>
      </table>

      <h2>Example (indicator schema)</h2>
      <pre><code>{`# Output of hr.fred.get_series("GDP", api_key)
# Columns:
#   date           datetime64[ns]  e.g. 2024-01-01
#   country_iso3   str             e.g. "USA"
#   indicator_id   str             e.g. "GDP"
#   value          float64         e.g. 27366.0
#   source         str             e.g. "FRED"`}</code></pre>
    </>
  );
}
