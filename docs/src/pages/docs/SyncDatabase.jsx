export default function SyncDatabaseDoc() {
  return (
    <>
      <h1><code>SyncDatabase</code></h1>
      <p><strong>File:</strong> <code>hermes/database/_sync.py</code></p>

      <h2>What It Does</h2>
      <p>
        Synchronous CRUD handle powered by SQLAlchemy 2.0. Every method opens its own
        session, auto-reflects table schemas, and commits on success. Supports PostgreSQL,
        SQLite, and any SQLAlchemy-compatible backend.
      </p>

      <h2>Bulk Insert Strategy</h2>
      <table>
        <thead>
          <tr><th>Scale</th><th>Method</th><th>Implementation</th></tr>
        </thead>
        <tbody>
          <tr><td>&lt; 100K rows</td><td><code>INSERT</code></td><td>Batched via <code>session.execute()</code> with periodic commit</td></tr>
          <tr><td>100K–10M</td><td><code>executemany</code></td><td>SQLAlchemy executemany mode</td></tr>
          <tr><td>10M+</td><td><code>COPY</code></td><td>Streams CSV via <code>StringIO</code> + <code>copy_expert()</code></td></tr>
        </tbody>
      </table>
      <p>The threshold for COPY (default 500K) is configurable via <code>bulk_copy_threshold</code>.</p>

      <h2>Methods</h2>

      <h3><code>insert(table, records, *, batch_size=50000) → int</code></h3>
      <pre><code>{`n = sync.insert("indicators", [
    {"date": "2024-01-01", "country_iso3": "USA",
     "indicator_id": "GDP", "value": 27366.0, "source": "FRED"},
    ...
], batch_size=10000)
print(f"Inserted {n} rows")`}</code></pre>

      <h3><code>upsert(table, records, conflict_columns, *, batch_size=50000) → int</code></h3>
      <p>Insert or update on conflict. Uses <code>INSERT ... ON CONFLICT DO UPDATE</code>.</p>
      <pre><code>{`n = sync.upsert("indicators", records,
    conflict_columns=["date", "country_iso3", "indicator_id"])`}</code></pre>

      <h3><code>update(table, filters, values) → int</code></h3>
      <pre><code>{`n = sync.update("indicators",
    {"country_iso3": "USA", "indicator_id": "GDP"},
    {"value": 28000.0})`}</code></pre>

      <h3><code>delete(table, filters) → int</code></h3>
      <pre><code>{`n = sync.delete("indicators",
    {"country_iso3": "USA", "indicator_id": {"like": "TEST_%"}})`}</code></pre>

      <h3><code>read(table, filters=None, *, columns=None, order_by=None, limit=None, offset=None, batch_size=None) → Iterator[list[dict]]</code></h3>
      <p>Returns an iterator of batches, each batch being a list of dicts.</p>
      <pre><code>{`for batch in sync.read("indicators",
    {"country_iso3": "USA"},
    columns=["date", "value"],
    order_by="date DESC",
    limit=100,
    batch_size=10):
    for row in batch:
        print(row["date"], row["value"])`}</code></pre>

      <h3><code>execute(sql, params=None) → CursorResult</code></h3>
      <pre><code>{`result = sync.execute("SELECT COUNT(*) FROM indicators")
count = result.scalar()`}</code></pre>

      <h3><code>raw_connection() → Connection</code></h3>
      <p>Returns the underlying DBAPI connection for direct use (e.g., PostgreSQL COPY).</p>

      <h3><code>close()</code></h3>
      <p>Dispose of the engine and release all connections.</p>

      <h2>Dynamic Filter System</h2>
      <p>
        Filters use a dict-based predicate language. Column names and types are auto-detected
        from the database — no hardcoded schema needed.
      </p>
      <pre><code>{`# Simple equality
{"country_iso3": "USA"}

# Comparison operators
{"value": {"gt": 100, "lte": 500}}

# IN / NOT IN
{"country_iso3": {"in": ["USA", "CAN"]}}

# Pattern matching
{"indicator_id": {"like": "GDP_%"}}

# NULL checks
{"value": None}  # or {"value": {"is": None}}

# Logical grouping
{"or": [{"value": {"lt": 0}}, {"source": "TEST"}]}

# NOT
{"not": {"country_iso3": "USA"}}`}</code></pre>
    </>
  );
}
