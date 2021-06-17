"""
Game class implementation module
"""
from random import Random
from time import perf_counter
from subprocess import run

from army import Army


class Game:

    _random = Random(12345)

    def __init__(self, armies):
        self.armies = armies

    @property
    def armies(self):
        return self._armies

    @armies.setter
    def armies(self, value):
        if not isinstance(value, list):
            raise TypeError("The `armies` must be a list value")

        value_len = len(value)
        if value_len < 2:
            raise ValueError("Amount value of armies cannot be less then 2")

        same_instances = value_len != len(set(value))

        for army in value:
            if not isinstance(army, Army) or same_instances:
                raise TypeError("Not all armies are correct instance")

        self._armies = value

    def select_attacking_and_defending_squads(self):
        result = {"attacking": None, "defending": None}
        alive_armies = [a for a in self.armies if a.is_active]
        attacking_army = self._random.choice(alive_armies)
        rest_armies = [a for a in alive_armies if a is not attacking_army]
        defending_army = self._random.choice(rest_armies)
        attacking_squads = [s for s in attacking_army.units if s.is_active]
        defending_squads = [s for s in defending_army.units if s.is_active]

        if attacking_squads and defending_squads:
            attacking = attacking_squads[0]
            defending = attacking.get_defending(defending_squads)
            result["attacking"] = attacking
            result["defending"] = defending

        return result

    def fight(self, now):
        participants = self.select_attacking_and_defending_squads()
        attacking = participants["attacking"]
        defending = participants["defending"]
        if attacking and defending:
            if attacking.success > defending.success:
                defending.get_damage(attacking.attack(now))

    def run_game(self):
        start = perf_counter()
        timer = 0
        while True:
            timer += 50
            run("clear", check=True)
            self.fight(timer)

            for army in self.armies:
                print(f"{army} health = {int(army.health)}:")
                print(army.health_line)

            alive_armies = [a for a in self.armies if a.is_active]
            if len(alive_armies) == 1:
                print("------------------------------------------------------")
                print(f"{alive_armies[0]} won!")
                print("---------------------")
                print(f"{int(perf_counter() - start)} seconds")
                print("------------------------------------------------------")
                return
