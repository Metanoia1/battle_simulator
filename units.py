"""Unit, Soldier, and Vehicle classes implementation module"""
from abc import ABCMeta, abstractmethod
from statistics import geometric_mean


class Unit(metaclass=ABCMeta):
    def __init__(self, recharge, random_, health=100):
        self.recharge = recharge
        self.random_ = random_
        self._health = health
        self.last_attack = 0

    @property
    def health(self):
        return self._health

    @property
    def last_attack(self):
        return self._last_attack

    @last_attack.setter
    def last_attack(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("last_attack value must be the int/float instance")
        self._last_attack = value

    def is_ready(self, now):
        return now - self.last_attack >= self.recharge

    @property
    @abstractmethod
    def success(self):
        """Returns attack success probability value"""

    @property
    @abstractmethod
    def is_active(self):
        """Returns True if unit is alive, else returns False"""

    @abstractmethod
    def attack(self, now):
        """Returns attack value and set self.last_attack"""

    @abstractmethod
    def get_damage(self, value):
        """Get damage from another unit"""


class Soldier(Unit):
    def __init__(self, random_, health=100, recharge=100, experience=0):
        super().__init__(recharge, random_, health)
        self.experience = experience

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        if not isinstance(value, int):
            raise TypeError("Experience value must be the (int) instance")

        self._experience = value

        if self.experience > 50:
            self._experience = 50

        if self.experience < 0:
            self._experience = 0

    @property
    def success(self):
        return (
            0.5
            * (1 + self.health / 100)
            * self.random_.randint(50 + self.experience, 100)
            / 100
        )

    @property
    def is_active(self):
        return self.health > 0

    def attack(self, now):
        self.last_attack = now
        current_experience = self.experience
        self.experience += 1
        return 0.05 + current_experience / 100

    def get_damage(self, value):
        self._health -= value


class Vehicle(Unit):
    def __init__(self, operators, random_, health=100, recharge=1001):
        super().__init__(recharge, random_, health)
        self.operators = operators

    @property
    def success(self):
        return (
            0.5
            * (1 + self.health / 100)
            * geometric_mean(o.success for o in self.operators)
        )

    @property
    def is_active(self):
        return self.health > 0 and any(o.is_active for o in self.operators)

    def attack(self, now):
        self.last_attack = now
        return 0.1 + sum(o.experience for o in self.operators) / 100

    def get_damage(self, value):
        percent_60 = value / 100 * 60
        percent_20 = value / 100 * 20
        self._health -= percent_60
        alive_operators = [o for o in self.operators if o.is_active]
        rest_operators = None

        if alive_operators:
            random_o = self.random_.choice(alive_operators)
            random_o.get_damage(percent_20)
            rest_operators = [o for o in alive_operators if o is not random_o]

        if rest_operators:
            value = percent_20 / max(len(rest_operators), 1)
            for operator in rest_operators:
                operator.get_damage(value)
