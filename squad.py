"""Squad class implementation module"""
from statistics import geometric_mean


class Squad:

    """Squad instance implementation"""

    def __init__(self, units, strategy, strategies):
        self.units = units
        self.strategy = strategy
        self.strategies = strategies

    @property
    def health(self):
        """Computed health value"""
        return sum(u.health for u in self.units if u.is_active)

    @property
    def is_active(self):
        """Returns True if any unit in self.units is alive, else returns False"""
        return any(u.is_active for u in self.units)

    @property
    def success(self):
        """Returns attack success probability value"""
        return geometric_mean(u.success for u in self.units)

    def attack(self, now: int) -> float:
        """Returns attack value"""
        return sum(u.attack(now) for u in self.units if u.is_ready(now))

    def get_damage(self, value):
        """Get damage from another unit"""
        alive_units = [u for u in self.units if u.is_active]
        value = value / max(len(alive_units), 1)
        for unit in alive_units:
            unit.get_damage(value)

    def get_defending(self, units):
        """Returns defending unit according to self.strategy"""
        return self.strategies[self.strategy](units)
