export default function MigrationsDoc() {
  return (
    <>
      <h1><code>MigrationRunner</code></h1>
      <p><strong>File:</strong> <code>hermes/database/_migrate.py</code></p>

      <h2>What It Does</h2>
      <p>
        Discovers <code>.sql</code> files in a <code>migrations/</code> directory and
        applies any that haven't been run yet. Tracks applied migrations in a
        <code>_schema_migrations</code> table with SHA-256 checksums to detect
        changes.
      </p>

      <h2>Architecture</h2>
      <p>The migration algorithm:</p>
      <ol>
        <li>Create <code>_schema_migrations</code> table if it doesn't exist</li>
        <li>Scan all <code>.sql</code> files in <code>migrations_dir</code>, sorted alphabetically</li>
        <li>For each file not yet in <code>_schema_migrations</code>:
          <ul>
            <li>Compute SHA-256 checksum</li>
            <li>Execute the entire file in a transaction</li>
            <li>Record the filename, checksum, and duration</li>
          </ul>
        </li>
        <li>If a previously-applied file's checksum has changed, log a warning but <strong>do not re-run</strong></li>
      </ol>

      <h2>Migration File Format</h2>
      <p>Files are named <code>NNN_description.sql</code> and sorted alphanumerically.</p>
      <pre><code>{`-- 001_create_indicators.sql
CREATE TABLE indicators (
    id            BIGSERIAL PRIMARY KEY,
    date          DATE NOT NULL,
    country_iso3  VARCHAR(3) NOT NULL,
    indicator_id  VARCHAR(50) NOT NULL,
    value         NUMERIC(20, 6),
    source        VARCHAR(20) NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_indicators_country ON indicators (country_iso3);`}</code></pre>

      <h2>Tracking Table</h2>
      <pre><code>{`_schema_migrations (
    filename    TEXT PRIMARY KEY,
    applied_at  TEXT,
    checksum    TEXT NOT NULL,
    duration_ms INTEGER DEFAULT 0
)`}</code></pre>

      <h2>Usage</h2>
      <p>Migrations run automatically when you create a <code>SyncDatabase</code>:</p>
      <pre><code>{`# Auto-runs all pending .sql files from ./migrations/
sync = db.sync_db("postgresql://...")

# Custom migrations directory
sync = db.sync_db("postgresql://...", migrations_dir="./db/migrations")`}</code></pre>
    </>
  );
}
