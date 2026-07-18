from hermes.database import DataBase
from hermes.sources.bis import BIS
from hermes.sources.fred import Fred
from hermes.sources.imf import IMF
from hermes.sources.world_bank import World_Bank
from hermes.storage import StorageLayer


class Hermes:

    def __init__(self):
        self.fred = Fred()
        self.world_bank = World_Bank()
        self.bis = BIS()
        self.imf = IMF()
        self._storage: StorageLayer | None = None

    @property
    def storage(self) -> StorageLayer:
        if self._storage is None:
            self._storage = StorageLayer()
            cache = self._storage.cache
            self.fred._cache = cache
            self.bis._cache = cache
            self.world_bank._cache = cache
            self.imf._cache = cache
        return self._storage
