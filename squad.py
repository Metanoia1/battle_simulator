"""
Squad class implementation module
"""
from strategies import get_weakest, get_strongest, get_random
from units import Unit, Soldier, Vehicle


class Squad(Unit):
    strategies = {
        "weakest": get_weakest,
        "strongest": get_strongest,
        "random": get_random,
    }

    def __init__(self, name, strategy, units):
        health = sum(u.health for u in units if u.is_active)
        recharge = sum(u.recharge for u in units if u.is_active)
        super().__init__(name, health, recharge)
        self.strategy = strategy
        self.units = units

    @property
    def health(self):
        return sum(u.health for u in self.units if u.is_active)

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, value):
        self._strategy = value

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if not isinstance(value, list):
            raise TypeError("The `units` must be a list value")

        if len(value) < 5 or len(value) > 10:
            raise ValueError("Amount value of units must be between 5-10")

        for unit in value:
            soldier_instance = isinstance(unit, Soldier)
            vehicle_instance = isinstance(unit, Vehicle)
            if not any([soldier_instance, vehicle_instance]):
                raise TypeError("Not all units are correct instance")

        self._units = value

    @property
    def success(self):
        units_scc = sum(u.success for u in self.units if u.is_active)
        units_len = max(len(self.units), 1)
        return units_scc / units_len

    def attack(self, now):
        return sum(
            u.attack(now)
            for u in self.units
            if u.is_active and u.is_ready(now)
        )

    def get_damage(self, value):
        alive_units = [u for u in self.units if u.is_active]
        alive_units_len = max(len(alive_units), 1)
        value = value / alive_units_len
        for unit in self.units:
            unit.get_damage(value)

    def get_defending(self, units):
        return self.strategies[self.strategy](units)
