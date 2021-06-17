"""
UnitsBuilder class implementation module
"""
from random import Random

from units import Soldier, Vehicle
from squad import Squad
from army import Army


class UnitsBuilder:

    _random = Random(12345)

    def __init__(self, army_name, strategy, squads_num, units_num):
        self._army_name = army_name
        self._strategy = strategy
        self._squads_num = squads_num
        self._units_num = units_num

    def create_soldier(self):
        return Soldier(self._army_name)

    def create_vehicle(self):
        soldiers = [self.create_soldier() for _ in range(3)]
        return Vehicle(self._army_name, soldiers)

    def create_squad(self):
        units = [self.create_soldier, self.create_vehicle]
        units = [self._random.choice(units)() for _ in range(self._units_num)]
        return Squad(self._army_name, self._strategy, units)

    def __call__(self):
        squads = [self.create_squad() for _ in range(self._squads_num)]
        strategy = self._strategy
        return Army(self._army_name, strategy, squads)
