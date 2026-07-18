export default function HermesDoc() {
  return (
    <>
      <h1><code>Hermes</code> Class</h1>
      <p><strong>File:</strong> <code>hermes/__init__.py</code></p>

      <h2>What It Does</h2>
      <p>
        The <code>Hermes</code> class is the top-level entry point for the Hermes SDK.
        It composes all connectors and the storage layer into a single unified interface.
      </p>

      <h2>Architecture</h2>
      <p>The <code>Hermes</code> class lazily initializes two subsystems:</p>
      <ul>
        <li><strong>Connectors</strong> — Created eagerly on <code>__init__</code>. Each connector (Fred, BIS, IMF, World Bank) is exposed as a property.</li>
        <li><strong>Storage</strong> — Created lazily on first access to <code>.storage</code>. When the storage layer is initialized, the RawCache is automatically wired to all connectors.</li>
      </ul>

      <h2>Usage</h2>
      <pre><code>{`from hermes import Hermes

hr = Hermes()

# Access connectors
hr.fred      # Fred connector
hr.bis       # BIS connector
hr.imf       # IMF connector
hr.world_bank # World Bank connector

# Access storage (lazy init)
hr.storage          # StorageLayer instance
hr.storage.cache    # RawCache (file-based Parquet cache)
hr.storage.features # FeatureStore (requires DB connection)
hr.storage.metadata # MetadataRegistry (requires DB connection)
hr.storage.lineage  # LineageGraph (requires DB connection)`}</code></pre>

      <h2>Cache Wiring</h2>
      <p>
        When <code>.storage</code> is accessed for the first time, the RawCache
        is automatically assigned to <code>fred._cache</code>, <code>bis._cache</code>,
        etc. This enables the <code>cached_get_series()</code> method on connectors
        to transparently read/write the Parquet cache.
      </p>

      <h2>Exports</h2>
      <p>The <code>hermes/__init__.py</code> also exports:</p>
      <pre><code>{`from hermes import Hermes
from hermes.base import BaseConnector
from hermes.countries import list_countries, get_country_metadata
from hermes._cache import DataCache`}</code></pre>
    </>
  );
}
