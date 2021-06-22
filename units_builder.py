"""UnitsBuilder class implementation module"""
from units import Soldier, Vehicle
from squad import Squad
from army import Army


class UnitsBuilder:

    """Instance of the UnitsBuilder class creates units for the game"""

    def __init__(self, strategy, squads_num, units_num, random_, strategies):
        self._strategy = strategy
        self._squads_num = squads_num
        self._units_num = units_num
        self._random = random_
        self._strategies = strategies

    def create_soldier(self, name):
        """This method creates Soldier instance

        Returns:
            Soldier instance
        """
        return Soldier(name, self._random)

    def create_vehicle(self, name):
        """This method creates Vehicle instance

        Returns:
            Vehicle instance
        """
        soldiers = [self.create_soldier(name) for _ in range(3)]
        return Vehicle(soldiers, name, self._random)

    def create_squad(self, name):
        """This method creates Squad instance

        Returns:
            Squad instance
        """
        soldiers_num = self._units_num // 2
        vehicles_num = self._units_num // 2

        if self._units_num % 2 != 0:
            soldiers_num += 1

        soldiers = [self.create_soldier(name) for _ in range(soldiers_num)]
        vehicles = [self.create_vehicle(name) for _ in range(vehicles_num)]

        units = soldiers + vehicles

        return Squad(
            units, name, self._strategy, self._random, self._strategies
        )

    def create_army(self, name):
        """This method creates Army instance

        Returns:
            Army instance
        """
        squads = [self.create_squad(name) for _ in range(self._squads_num)]
        return Army(
            squads, name, self._strategy, self._random, self._strategies
        )
