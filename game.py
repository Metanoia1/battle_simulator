"""Game class implementation module"""
# pylint: disable=(no-self-use)
from subprocess import run
from typing import List

from utils import mylogger
from army import Army


class Game:

    """This class implements the lifecycle of the game"""

    def __init__(self, armies: List[Army]) -> None:
        self.armies = armies

    def _get_defending_army(self, army):
        armies = [a for a in self.armies if a is not army and a.is_active]
        if armies:
            return army.get_defending(armies)
        return None

    def _get_defending_squad(self, defending_army, attacking_squad):
        defending_squads = [s for s in defending_army.units if s.is_active]
        if defending_squads:
            return attacking_squad.get_defending(defending_squads)
        return None

    def _attack(self, attacking_squad, defending_squad, now):
        if attacking_squad and defending_squad:
            if attacking_squad.success > defending_squad.success:
                defending_squad.get_damage(attacking_squad.attack(now))

    def _squads_fight(self, attacking_squads, defending_army, now):
        for squad in attacking_squads:
            if squad.is_active:
                self._attack(
                    squad,
                    self._get_defending_squad(defending_army, squad),
                    now,
                )

    def fight(self, now: int):
        """Implements one round of the fight

        Returns (Army) if that is an only alive army in self.armies else:
        returns (None)
        """
        for army in self.armies:
            if army.is_active:
                defending_army = self._get_defending_army(army)

                if not defending_army:
                    return army

                mylogger(army, defending_army)
                self._squads_fight(army.units, defending_army, now)

        return None

    def run_game(self) -> None:
        """launches the lifecycle of the game"""
        timer = 0
        while True:
            timer += 100
            run("clear", check=True)

            for army in self.armies:
                print(army)
                print(army.health_line)

            winner = self.fight(timer)

            if winner:
                print("_" * 20)
                print(f"{winner.name} won!")
                print("_" * 20)
                return
