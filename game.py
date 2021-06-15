"""
Game class implementation module
"""
from random import choice
from time import perf_counter
from subprocess import run

from army import Army


class Game:
    def __init__(self, armies):
        self.armies = armies

    @property
    def armies(self):
        return self._armies

    @armies.setter
    def armies(self, value):
        if not isinstance(value, set):
            raise TypeError("The `armies` must be a set value")

        if len(value) < 2:
            raise ValueError("Amount value of armies cannot be less then 2")

        for army in value:
            if not isinstance(army, Army):
                raise TypeError("Not all armies are correct instance")

        self._armies = value

    def select_attacking_and_defending_squads(self):
        result = {"attacking": None, "defending": None}

        alive_armies = [a for a in self.armies if a.is_active]
        attacking_army = choice(alive_armies)
        rest_armies = [a for a in alive_armies if a is not attacking_army]
        defending_army = choice(rest_armies)
        attacking_squads = [s for s in attacking_army.squads if s.is_active]
        defending_squads = [s for s in defending_army.squads if s.is_active]

        if attacking_squads and defending_squads:
            attacking_squad = choice(attacking_squads)
            d_squads = defending_squads
            func = lambda squad: squad.health

            if attacking_squad.strategy == "weakest":
                defending_squad = sorted(d_squads, key=func)[0]

            if attacking_squad.strategy == "strongest":
                defending_squad = sorted(d_squads, key=func, reverse=True)[0]

            if attacking_squad.strategy == "random":
                defending_squad = choice(d_squads)

            result["attacking"] = attacking_squad
            result["defending"] = defending_squad

        return result

    def fight(self):
        participants = self.select_attacking_and_defending_squads()
        attacking = participants["attacking"]
        defending = participants["defending"]
        if attacking and defending:
            if attacking.success > defending.success:
                defending.get_damage(attacking.attack())

    def run_game(self):
        start = perf_counter()
        while True:
            run("clear", check=True)

            self.fight()

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
