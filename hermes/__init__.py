from hermes.sources.fred import Fred
from hermes.sources.world_bank import World_Bank
from hermes.sources.bis import BIS

class Hermes:

    def __init__(self):
        self.fred = Fred()
        self.world_bank = World_Bank()
        self.bis = BIS()
