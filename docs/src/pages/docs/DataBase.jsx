export default function DataBaseDoc() {
  return (
    <>
      <h1><code>DataBase</code> Factory</h1>
      <p><strong>File:</strong> <code>hermes/database/__init__.py</code></p>

      <h2>What It Does</h2>
      <p>
        The <code>DataBase</code> class is a factory that provisions a fully-configured
        database in one function call. It connects to the database, runs all pending
        SQL migrations, and returns a CRUD handle.
      </p>

      <h2>Architecture</h2>
      <p>
        The factory separates concerns into three layers:
      </p>
      <ul>
        <li><strong><code>DataBase</code></strong> — Factory class. No state. Each call creates an independent database handle.</li>
        <li><strong><code>SyncDatabase</code></strong> — Synchronous CRUD handle with batch insert, upsert, streaming reads, and COPY support.</li>
        <li><strong><code>AsyncDatabase</code></strong> — Mirror of SyncDatabase with <code>async def</code> / <code>async for</code>.</li>
      </ul>

      <h2>Usage</h2>
      <pre><code>{`from hermes import DataBase

db = DataBase()

# Sync — connects, runs migrations, returns handle
sync = db.sync_db("postgresql://user:pass@localhost:5432/hermes")
# Or with SQLite (for development/testing)
sync = db.sync_db("sqlite:///hermes.db")

# Async
import asyncio
async_db = await db.async_db("postgresql+asyncpg://user:pass@localhost:5432/hermes")`}</code></pre>

      <h2>Configuration</h2>
      <pre><code>{`sync = db.sync_db(
    url="postgresql://user:pass@host:5432/hermes",
    migrations_dir="./migrations",  # default
    bulk_copy_threshold=500_000,     # switch to COPY at 500K rows
    strict_filters=False,            # raise on unknown filter columns?
    pool_size=10, max_overflow=20,   # engine kwargs
)`}</code></pre>
    </>
  );
}
