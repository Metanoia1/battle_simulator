"""Unit, Soldier, and Vehicle classes implementation module"""
from abc import ABCMeta, abstractmethod
from statistics import geometric_mean


class Unit(metaclass=ABCMeta):
    def __init__(self, name, health, recharge, random_):
        self.name = name
        self._init_health = health
        self.health = health
        self.recharge = recharge
        self.random_ = random_
        self.last_attack = 0

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise TypeError("health must be int/float")

        if value > 10000:
            raise ValueError("health cannot be more than 10000")

        self._health = value

        if self.health > self._init_health:
            self._health = self._init_health

        if self.health < 0:
            self._health = 0

    @property
    @abstractmethod
    def success(self):
        """Returns attack success probability value"""

    @abstractmethod
    def attack(self, now):
        """Returns attack value and set self.last_attack"""

    @abstractmethod
    def get_damage(self, value):
        """Get damage from another unit"""

    @property
    @abstractmethod
    def is_active(self):
        """Returns True if unit is alive, else returns False"""

    @property
    def last_attack(self):
        return self._last_attack

    @last_attack.setter
    def last_attack(self, value):
        value_int = isinstance(value, int)
        value_float = isinstance(value, float)
        if not any([value_int, value_float]):
            raise TypeError("`last_attack` must be int/float instance")

        self._last_attack = value

    @property
    def health_line(self):
        health_line_len = 50
        health_line_symbol = "."
        health_percent = self.health / self._init_health * 100
        health_line_int = int(health_line_len / 100 * health_percent)
        return health_line_symbol * health_line_int

    def is_ready(self, now):
        return now - self.last_attack >= self.recharge

    def __repr__(self):
        print_health = int(self.health)
        return f"{self.__class__.__name__}-{self.name} health-{print_health}"


class Soldier(Unit):
    def __init__(self, name, random_, health=100, recharge=100, experience=0):
        super().__init__(name, health, recharge, random_)
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
        value_1 = 0.5
        value_2 = 1 + self.health / 100
        value_3 = self.random_.randint(50 + self.experience, 100)
        one_hundred = 100
        return value_1 * value_2 * value_3 / one_hundred

    def attack(self, now):
        self.last_attack = now
        current_experience = self.experience
        self.experience += 1
        value = 0.05
        return value + current_experience / 100

    def get_damage(self, value):
        self.health -= value

    @property
    def is_active(self):
        return self.health > 0


class Vehicle(Unit):
    def __init__(self, operators, name, random_, health=100, recharge=1001):
        super().__init__(name, health, recharge, random_)
        self.operators = operators

    @property
    def success(self):
        value_1 = 0.5
        value_2 = 1 + self.health / 100
        value_3 = geometric_mean(o.success for o in self.operators)
        return value_1 * value_2 * value_3

    def attack(self, now):
        self.last_attack = now
        value = 0.1
        operators_ex = sum(o.experience for o in self.operators)
        one_hundred = 100
        return value + operators_ex / one_hundred

    def get_damage(self, value):
        percent_60 = value / 100 * 60
        percent_20 = value / 100 * 20
        self.health -= percent_60
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

    @property
    def is_active(self):
        return self.health > 0 and any(o.is_active for o in self.operators)
