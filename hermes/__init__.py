from hermes.database import DataBase
from hermes.sources.bis import BIS
from hermes.sources.fred import Fred
from hermes.sources.imf import IMF
from hermes.sources.world_bank import World_Bank


class Hermes:

    def __init__(self):
        self.fred = Fred()
        self.world_bank = World_Bank()
        self.bis = BIS()
        self.imf = IMF()

