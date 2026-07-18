export default function AsyncDatabaseDoc() {
  return (
    <>
      <h1><code>AsyncDatabase</code></h1>
      <p><strong>File:</strong> <code>hermes/database/_async.py</code></p>

      <h2>What It Does</h2>
      <p>
        Async mirror of <code>SyncDatabase</code>. All CRUD methods are
        <code>async def</code> and <code>read()</code> returns
        <code>AsyncIterator[list[dict]]</code>.
        Uses <code>create_async_engine</code> from SQLAlchemy's asyncio extension
        (requires <code>asyncpg</code> for PostgreSQL or <code>aiosqlite</code> for SQLite).
      </p>

      <h2>Architecture</h2>
      <p>
        Similar to SyncDatabase, with key differences:
      </p>
      <ul>
        <li>Engine created via <code>create_async_engine("postgresql+asyncpg://...")</code></li>
        <li>Session via <code>async_sessionmaker</code> with <code>expire_on_commit=False</code></li>
        <li><code>_reflect()</code> uses <code>conn.run_sync()</code> for schema introspection</li>
        <li>Table reflection is cached in <code>_reflect_cache</code> dict</li>
        <li>Migrations run on first <code>await database.initialize()</code></li>
      </ul>

      <h2>Usage</h2>
      <pre><code>{`from hermes import DataBase

db = DataBase()
async_db = await db.async_db("postgresql+asyncpg://user:pass@localhost:5432/hermes")

# Insert
n = await async_db.insert("indicators", [
    {"date": "2024-01-01", "country_iso3": "USA",
     "indicator_id": "GDP", "value": 27366.0, "source": "FRED"}
])

# Read (async iteration)
async for batch in async_db.read("indicators",
    {"country_iso3": "USA"},
    batch_size=1000):
    for row in batch:
        print(row)

# Upsert
n = await async_db.upsert("indicators",
    new_records,
    conflict_columns=["date", "country_iso3", "indicator_id"])

# Cleanup
await async_db.close()`}</code></pre>

      <h2>Important</h2>
      <p>
        The <code>AsyncDatabase</code> does NOT run migrations in the constructor
        (unlike <code>SyncDatabase</code>). Instead, migrations are run when
        <code>await db.initialize()</code> is called, which is handled automatically
        by the <code>DataBase.async_db()</code> factory method.
      </p>
    </>
  );
}
