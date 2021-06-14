"""
UnitsBuilder class implementation module
"""
from random import randint, choice

from units import Soldier, Vehicle
from squad import Squad
from army import Army


class UnitsBuilder:
    def __init__(self, army_name, units_num, squads_num):
        self._army_name = army_name
        self._units_num = units_num
        self._squads_num = squads_num
        self._strategy = ("weakest", "strongest", "random")

    def create_soldier(self, health=100, recharge=100, experience=0):
        recharge = randint(recharge, 2000)
        return Soldier(health, recharge, experience)

    def create_vehicle(self, health=100, recharge=1001):
        soldiers = {self.create_soldier() for _ in range(randint(1, 3))}
        recharge = randint(recharge, 2000)
        return Vehicle(soldiers, health, recharge)

    def create_squad(self, strategy=None):
        if not strategy:
            strategy = choice(self._strategy)
        units = [self.create_soldier, self.create_vehicle]
        units = {choice(units)() for _ in range(self._units_num)}
        return Squad(strategy, units)

    def create_army(self, strategy):
        squads = {self.create_squad(strategy) for _ in range(self._squads_num)}
        return Army(self._army_name, squads)

    def __call__(self):
        squads = {self.create_squad() for _ in range(self._squads_num)}
        return Army(self._army_name, squads)
