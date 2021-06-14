"""
Squad class implementation module
"""
from units import Soldier, Vehicle


class Squad:
    def __init__(self, strategy, units):
        self.strategy = strategy
        self.units = units

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        if value == "weakest":
            self._strategy = "weakest"
        elif value == "strongest":
            self._strategy = "strongest"
        else:
            self._strategy = "random"

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if not isinstance(value, set):
            raise TypeError("The `units` must be a set value")

        if len(value) < 5 or len(value) > 10:
            raise ValueError("Amount value of units must be between 5-10")

        for unit in value:
            soldier_instance = isinstance(unit, Soldier)
            vehicle_instance = isinstance(unit, Vehicle)
            if not any([soldier_instance, vehicle_instance]):
                raise TypeError("Not all units are correct instance")

        self._units = value

    @property
    def health(self):
        return sum(u.health for u in self.units if u.is_active)

    @property
    def is_active(self):
        alive_units = [u for u in self.units if u.is_active]
        if alive_units:
            return True
        return False

    def success(self):
        units_scc = sum(u.success() for u in self.units if u.is_active)
        units_len = max(len(self.units), 1)
        return units_scc / units_len

    def attack(self):
        # and u.is_ready
        return sum(u.attack() for u in self.units if u.is_active)

    def get_damage(self, value):
        alive_units = [u for u in self.units if u.is_active]
        alive_units_len = max(len(alive_units), 1)
        value = value / alive_units_len
        for unit in self.units:
            unit.health -= value
