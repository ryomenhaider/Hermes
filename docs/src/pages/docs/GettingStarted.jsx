export default function GettingStarted() {
  return (
    <>
      <h1>Getting Started</h1>

      <h2>Installation</h2>
      <pre><code>{`# Clone the repository
git clone https://github.com/ryomenhaider/Hermes.git
cd Hermes

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .`}</code></pre>

      <h2>Quick Start</h2>
      <pre><code>{`from hermes import Hermes, DataBase

# Initialize the SDK
hr = Hermes()

# Fetch economic data from FRED
fred_api = hr.fred.connect("YOUR_FRED_API_KEY")
gdp = hr.fred.get_series("GDP", fred_api)
print(gdp.head())`}</code></pre>

      <h2>Environment Setup</h2>
      <p>Create a <code>.env</code> file in the project root:</p>
      <pre><code>{`FRED_API=your_fred_api_key_here`}</code></pre>
      <p>FRED requires a free API key (any email). BIS, IMF, and World Bank require no authentication.</p>

      <h2>Architecture Overview</h2>
      <p>Hermes is organized into three layers:</p>
      <table>
        <thead>
          <tr><th>Layer</th><th>Path</th><th>Purpose</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Connectors</strong></td><td><code>hermes/sources/</code></td><td>Fetch data from 30+ free APIs, normalize to canonical DataFrames</td></tr>
          <tr><td><strong>Database</strong></td><td><code>hermes/database/</code></td><td>One-function DB provisioning, migrations, CRUD with dynamic filters</td></tr>
          <tr><td><strong>Storage</strong></td><td><code>hermes/storage/</code></td><td>Parquet caching, feature store, metadata registry, lineage tracking</td></tr>
        </tbody>
      </table>

      <h2>Quick Example — Full Pipeline</h2>
      <pre><code>{`from hermes import Hermes, DataBase
import os

hr = Hermes()

# 1. Connect to a database
db = DataBase()
sync = db.sync_db("sqlite:///hermes.db")

# 2. Connect storage
hr.storage.connect("sqlite:///hermes.db")

# 3. Fetch data
fred_key = hr.fred.connect(os.getenv("FRED_API"))
gdp = hr.fred.get_series("GDP", fred_key)

# 4. Store as features
hr.storage.features.store(gdp, "gdp_timeseries", version=1)

# 5. Track metadata
hr.storage.metadata.register("FRED", "GDP",
    row_count=len(gdp), quality_score=0.95)

# 6. Trace lineage
hr.storage.lineage.record("gdp_v1", "FRED",
    pipeline_name="fred_pipeline", pipeline_version=1)

print(hr.storage.metadata.staleness_report())`}</code></pre>
    </>
  );
}
