from hermes.database._async import AsyncDatabase
from hermes.database._sync import SyncDatabase


class DataBase:
    def sync_db(self, url: str, migrations_dir: str = "./migrations", **kwargs) -> SyncDatabase:
        return SyncDatabase(url, migrations_dir=migrations_dir, **kwargs)

    async def async_db(self, url: str, migrations_dir: str = "./migrations", **kwargs) -> AsyncDatabase:
        db = AsyncDatabase(url, migrations_dir=migrations_dir, **kwargs)
        await db.initialize()
        return db
