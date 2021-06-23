"""Game class implementation module"""
from subprocess import run

from utils import mylogger


class Game:
    def __init__(self, armies):
        self.armies = armies

    def _get_defending_army(self, attacking_army):
        defending_armies = [
            a for a in self.armies if a is not attacking_army and a.is_active
        ]
        if defending_armies:
            return attacking_army.get_defending(defending_armies)
        return None

    def _get_defending_squad(self, defending_army, attacking_squad):
        defending_squads = [s for s in defending_army.units if s.is_active]
        if defending_squads:
            return attacking_squad.get_defending(defending_squads)
        return None

    def fight(self, attacking_squad, defending_squad, now):
        if attacking_squad and defending_squad:
            if attacking_squad.success > defending_squad.success:
                defending_squad.get_damage(attacking_squad.attack(now))

    def move(self, now):
        for army in self.armies:
            if army.is_active:
                defending_army = self._get_defending_army(army)

                if not defending_army:
                    return army

                mylogger(army, defending_army)
                for squad in army.units:
                    if squad.is_active:
                        defending_squad = self._get_defending_squad(
                            defending_army, squad
                        )
                        self.fight(squad, defending_squad, now)
        return None

    def run_game(self):
        timer = 0
        while True:
            timer += 100
            run("clear", check=True)

            for army in self.armies:
                print(army)
                print(army.health_line)

            winner = self.move(timer)

            if winner:
                print("_" * 20)
                print(f"{winner.name} won!")
                print("_" * 20)
                return
