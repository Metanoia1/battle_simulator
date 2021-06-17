"""
Module to start the game
"""
import json

from game import Game
from units_builder import UnitsBuilder


def get_data_from_json_file(filename):
    with open(filename) as json_file:
        result = json.load(json_file)
    return result


def main():
    data = get_data_from_json_file("config.json")

    armies_num = data["number_of_armies"]
    strategy = data["armies_strategy"]
    squads_per_army = data["squads_per_army"]
    units_per_squad = data["units_per_squad"]

    armies = [
        UnitsBuilder(
            f"ARMY_{army+1}", strategy, squads_per_army, units_per_squad
        )()
        for army in range(armies_num)
    ]

    game = Game(armies)
    game.run_game()


if __name__ == "__main__":
    main()
