"""
Army class implementation module
"""
from squad import Squad


class Army:
    def __init__(self, name, squads):
        self.name = name
        self.squads = squads
        self._init_health = sum(s.health for s in self.squads if s.is_active)
        self._health_line_symbol = "."
        self._health_line_len = 50

    @property
    def squads(self):
        return self._squads

    @squads.setter
    def squads(self, value):
        if not isinstance(value, set):
            raise TypeError("The `squads` must be a set value")

        if len(value) < 2:
            raise ValueError("Amount value of squads cannot be less then 2")

        for squad in value:
            if not isinstance(squad, Squad):
                raise TypeError("Not all squads are correct instance")

        self._squads = value

    @property
    def health(self):
        return sum(s.health for s in self.squads if s.is_active)

    @property
    def health_line(self):
        health_percent = self.health / self._init_health * 100
        health_line_int = int(self._health_line_len / 100 * health_percent)
        return self._health_line_symbol * health_line_int

    @property
    def is_active(self):
        alive_squads = [s for s in self.squads if s.is_active]
        if alive_squads:
            return True
        return False

    def __str__(self):
        return self.name
