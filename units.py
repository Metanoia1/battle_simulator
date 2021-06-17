"""
Unit, Soldier, and Vehicle classes implementation module
"""
from abc import ABCMeta, abstractmethod
from random import Random
from statistics import geometric_mean


class Unit(metaclass=ABCMeta):

    _random = Random(12345)

    def __init__(self, name, health, recharge):
        self._init_health = health
        self._health_line_symbol = "."
        self._health_line_len = 50

        self.name = name
        self.recharge = recharge
        self.now = 0

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be the (str) instance")

        value = value.strip()
        value_len = len(value)
        if value_len < 3 or value_len > 15:
            raise ValueError("Name value must be between 3-15 symbols")

        self._name = value

    @property
    def recharge(self):
        return self._recharge

    @recharge.setter
    def recharge(self, value):
        if not isinstance(value, int):
            raise TypeError("Recharge value must be (int) instance")

        if value < 100:
            raise ValueError("Recharge value cannot be less than 100")

        self._recharge = value

        if self.recharge > 2000:
            self._recharge = value

    @property
    def now(self):
        return self._now

    @now.setter
    def now(self, value):
        value_int = isinstance(value, int)
        value_float = isinstance(value, float)
        if not any([value_int, value_float]):
            raise TypeError("The `now` value must be an int/float instance")

        self._now = value

    @property
    def health_line(self):
        health_percent = self.health / self._init_health * 100
        health_line_int = int(self._health_line_len / 100 * health_percent)
        return self._health_line_symbol * health_line_int

    @property
    def is_active(self):
        return self.health > 0

    def is_ready(self, now):
        return now - self.now >= self.recharge

    @property
    @abstractmethod
    def health(self):
        "Returns health value"

    @property
    @abstractmethod
    def success(self):
        "Returns attack success probability value"

    @abstractmethod
    def attack(self, now):
        "Returns attack value and set self.now"

    @abstractmethod
    def get_damage(self, value):
        "Get damage from another unit"

    def __str__(self):
        return self.name


class Soldier(Unit):
    def __init__(self, name, health=100, recharge=100, experience=0):
        super().__init__(name, health, recharge)
        self._health = health
        self.experience = experience

    @property
    def health(self):
        return self._health

    @property
    def experience(self):
        return self._experience

    @experience.setter
    def experience(self, value):
        if not isinstance(value, int):
            raise TypeError("Experience value must be the (int) instance")

        if value > 50:
            self._experience = 50
        elif value < 0:
            self._experience = 0
        else:
            self._experience = value

    @property
    def success(self):
        value_1 = 0.5
        value_2 = 1 + self.health / 100
        value_3 = self._random.randint(50 + self.experience, 100)
        one_hundred = 100
        return value_1 * value_2 * value_3 / one_hundred

    def attack(self, now):
        self.now = now
        self.experience += 1
        value = 1  # 0.05
        return value + self.experience / 100

    def get_damage(self, value):
        self._health -= value


class Vehicle(Unit):
    def __init__(self, name, operators, health=100, recharge=1001):
        super().__init__(name, health, recharge)
        self._health = health
        self.operators = operators

    @property
    def health(self):
        return self._health

    @property
    def operators(self):
        return self._operators

    @operators.setter
    def operators(self, value):
        if not isinstance(value, list):
            raise TypeError("The `operators` value must be a list value")

        if len(value) < 1 or len(value) > 3:
            raise ValueError("Amount value of operators must be between 1-3")

        for operator in value:
            if not isinstance(operator, Soldier):
                raise TypeError("All operators must be the Soldier instance")

        self._operators = value

    @property
    def success(self):
        value_1 = 0.5
        value_2 = 1 + self.health / 100
        value_3 = [o.success for o in self.operators if o.is_active]
        gavg = geometric_mean(value_3)
        return value_1 * value_2 * gavg

    def attack(self, now):
        self.now = now
        value = 2  # 0.1
        operators_ex = sum(o.experience for o in self.operators if o.is_active)
        one_hundred = 100
        return value + operators_ex / one_hundred

    def get_damage(self, value):
        percent_60 = value / 100 * 60
        percent_20 = value / 100 * 20
        self._health -= percent_60
        alive_operators = [o for o in self.operators if o.is_active]
        rest_operators = None

        if alive_operators:
            random_o = self._random.choice(alive_operators)
            random_o.get_damage(percent_20)
            rest_operators = [o for o in alive_operators if o is not random_o]

        if rest_operators:
            value = percent_20 / len(rest_operators)
            for operator in rest_operators:
                operator.get_damage(value)

        alive_operators = [o for o in self.operators if o.is_active]

        if self.health <= 0 or not alive_operators:
            self._health = 0
            for operator in self.operators:
                operator._health = 0
