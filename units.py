"""
Unit, Soldier, and Vehicle classes implementation module
"""
from random import randint, choice
from time import perf_counter
from statistics import geometric_mean


class Unit:
    def __init__(self, health, recharge):
        self.now = perf_counter()
        self._init_health = health
        self.health = health
        self.recharge = recharge

    @property
    def now(self):
        return self._now

    @now.setter
    def now(self, value):
        value = perf_counter()
        self._now = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        float_instance = isinstance(value, float)
        int_instance = isinstance(value, int)
        if not any([float_instance, int_instance]):
            raise TypeError("Health value must be the int/float instance")

        if value > 10000:
            raise ValueError("Health value cannot be more than 10000")

        if value > self._init_health:
            self._health = self._init_health
        elif value < 0:
            self._health = 0
        else:
            self._health = value

    @property
    def recharge(self):
        return self._recharge

    @recharge.setter
    def recharge(self, value):
        if not isinstance(value, int):
            raise TypeError("Recharge value must be (int) instance")

        if value < 100 or value > 2000:
            raise ValueError("Recharge value must be between 100-2000")

        self._recharge = value

    @property
    def is_active(self):
        if self.health > 0:
            return True
        return False

    @property
    def is_ready(self):
        if perf_counter() - self.now >= self.recharge * 0.001:
            return True
        return False


class Soldier(Unit):
    def __init__(self, health=100, recharge=100, experience=0):
        super().__init__(health, recharge)
        self._experience = experience

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
        value_3 = randint(50 + self.experience, 100)
        one_hundred = 100
        return value_1 * value_2 * value_3 / one_hundred

    def attack(self):
        self.now = perf_counter()
        self.experience += 1
        value = 1  # 0.05
        return value + self.experience / 100

    def get_damage(self, value):
        self.health -= value


class Vehicle(Unit):
    def __init__(self, operators, health=100, recharge=1001):
        super().__init__(health, recharge)
        self.operators = operators

    @property
    def operators(self):
        return self._operators

    @operators.setter
    def operators(self, value):
        if not isinstance(value, set):
            raise TypeError("The `operators` value must be a set value")

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

    def attack(self):
        self.now = perf_counter()
        value = 2  # 0.1
        operators_ex = sum(o.experience for o in self.operators if o.is_active)
        one_hundred = 100
        return value + operators_ex / one_hundred

    def get_damage(self, value):
        self.health -= value / 60 * 100
        alive_operators = [o for o in self.operators if o.is_active]
        random_o = choice(alive_operators)
        random_o.health -= value / 20 * 100
        rest_operators = [o for o in alive_operators if o is not random_o]

        for operator in rest_operators:
            operator.health -= value / 10 * 100

        alive_operators = [o for o in self.operators if o.is_active]

        if self.health <= 0 or not alive_operators:
            self.health = 0
            for operator in self.operators:
                operator.health = 0
