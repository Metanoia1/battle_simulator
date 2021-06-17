"""
Army class implementation module
"""
from squad import Squad


class Army(Squad):
    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if not isinstance(value, list):
            raise TypeError("The `units` must be a list value")

        if len(value) < 2 or len(value) > 10:
            raise ValueError("Amount value of units must be between 2-10")
        print(value)

        for unit in value:
            if not isinstance(unit, Squad):
                raise TypeError("Not all units are correct instance")

        self._units = value
