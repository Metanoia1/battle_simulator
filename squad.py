"""Squad class implementation module"""
from statistics import geometric_mean


class Squad:
    def __init__(self, units, strategy, strategies):
        self.units = units
        self.strategy = strategy
        self.strategies = strategies

    @property
    def health(self):
        return sum(u.health for u in self.units if u.is_active)

    @property
    def is_active(self):
        return any(u.is_active for u in self.units)

    @property
    def success(self):
        return geometric_mean(u.success for u in self.units)

    def attack(self, now):
        return sum(u.attack(now) for u in self.units if u.is_ready(now))

    def get_damage(self, value):
        alive_units = [u for u in self.units if u.is_active]
        value = value / max(len(alive_units), 1)
        for unit in alive_units:
            unit.get_damage(value)

    def is_ready(self, now):
        return all(u.is_ready(now) for u in self.units)

    def get_defending(self, units):
        return self.strategies[self.strategy](units)
