"""UnitsBuilder class implementation module"""
from units import Soldier, Vehicle
from squad import Squad
from army import Army


class UnitsBuilder:

    """Instance of the UnitsBuilder class creates units for the game"""

    def __init__(self, strategies, strategy, squads_num, units_num, random_):
        self._strategies = strategies
        self._strategy = strategy
        self._squads_num = squads_num
        self._units_num = units_num
        self.random_ = random_

    def create_soldier(self):
        """This method creates Soldier instance

        Returns:
            Soldier instance
        """
        return Soldier(self.random_)

    def create_vehicle(self):
        """This method creates Vehicle instance

        Returns:
            Vehicle instance
        """
        soldiers = [self.create_soldier() for _ in range(3)]
        return Vehicle(soldiers, self.random_)

    def create_squad(self):
        """This method creates Squad instance

        Returns:
            Squad instance
        """
        soldiers_num = self._units_num // 2
        vehicles_num = self._units_num // 2

        if self._units_num % 2 != 0:
            soldiers_num += 1

        soldiers = [self.create_soldier() for _ in range(soldiers_num)]
        vehicles = [self.create_vehicle() for _ in range(vehicles_num)]
        units = soldiers + vehicles
        return Squad(units, self._strategy, self._strategies)

    def create_army(self, name):
        """This method creates Army instance

        Returns:
            Army instance
        """
        squads = [self.create_squad() for _ in range(self._squads_num)]
        return Army(name, squads, self._strategy, self._strategies)
