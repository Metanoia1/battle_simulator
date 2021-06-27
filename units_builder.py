"""UnitsBuilder class implementation module"""
from army import Army
from squad import Squad
from units import Soldier, Vehicle


class UnitsBuilder:

    """Instance of the UnitsBuilder class creates units for the game"""

    def __init__(self, strategy, strategies, squads_num, units_num, random_):
        self._strategy = strategy
        self._strategies = strategies
        self._squads_num = squads_num
        self._units_num = units_num
        self.random_ = random_

    def create_soldier(self, health=100, recharge=100, exp=0) -> Soldier:
        """This method creates Soldier instance"""
        return Soldier(self.random_, health, recharge, exp)

    def create_vehicle(self, health=100, recharge=1001) -> Vehicle:
        """This method creates Vehicle instance"""
        operators = [self.create_soldier() for _ in range(3)]
        return Vehicle(operators, self.random_, health, recharge)

    def create_squad(self) -> Squad:
        """This method creates Squad instance"""
        soldiers_num = self._units_num // 2
        vehicles_num = self._units_num // 2

        if self._units_num % 2 != 0:
            soldiers_num += 1

        soldiers = [self.create_soldier() for _ in range(soldiers_num)]
        vehicles = [self.create_vehicle() for _ in range(vehicles_num)]
        units = soldiers + vehicles
        return Squad(units, self._strategy, self._strategies)

    def create_army(self, name: str) -> Army:
        """This method creates Army instance"""
        squads = [self.create_squad() for _ in range(self._squads_num)]
        return Army(name, squads, self._strategy, self._strategies)
