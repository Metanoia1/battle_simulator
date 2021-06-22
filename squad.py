"""
Squad class implementation module
"""
from statistics import geometric_mean

from units import Unit


class Squad(Unit):
    def __init__(self, units, name, strategy, random_, strategies):
        recharge = sum(u.recharge for u in units)
        health = sum(u.health for u in units if u.is_active)
        super().__init__(name, health, recharge, random_)
        self.units = units
        self.strategy = strategy
        self.strategies = strategies
        self._init_health = sum(u.health for u in self.units)

    @property
    def health(self):
        return sum(u.health for u in self.units if u.is_active)

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def success(self):
        return geometric_mean(u.success for u in self.units)

    def attack(self, now):
        self.last_attack = now
        return sum(u.attack(now) for u in self.units if u.is_ready(now))

    def get_damage(self, value):
        alive_units = [u for u in self.units if u.is_active]
        alive_units_len = max(len(alive_units), 1)
        value = value / alive_units_len
        for unit in alive_units:
            unit.get_damage(value)

    def get_defending(self, units):
        return self.strategies[self.strategy](units)

    def is_ready(self, now):
        return all(u.is_ready(now) for u in self.units if u.is_active)

    @property
    def is_active(self):
        return any(u.is_active for u in self.units)
