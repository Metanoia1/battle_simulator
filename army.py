"""Army class implementation module"""
from squad import Squad


class Army(Squad):

    """This class describes an army instance"""

    def __init__(self, name, units, strategy, strategies):
        super().__init__(units, strategy, strategies)
        self.name = name
        self._init_health = sum(u.health for u in self.units)

    @property
    def health_line(self):
        """Visual line of the health status"""
        health_line_len = 50
        health_line_symbol = "."
        health_percent = self.health / self._init_health * 100
        health_line_int = int(health_line_len / 100 * health_percent)
        return health_line_symbol * health_line_int

    def __repr__(self):
        if self.health > 0 and self.health < 1:
            return f"{self.name} health: {self.health}"
        return f"{self.name} health: {int(self.health)}"
