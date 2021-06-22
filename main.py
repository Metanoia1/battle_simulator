"""
Module to start the game
"""
from random import Random

from units_builder import UnitsBuilder
from services import get_data_from_json_file, clear_log
from strategies import all_strategies
from game import Game


def main():
    clear_log()
    data = get_data_from_json_file("config.json")
    armies_num = data["number_of_armies"]
    strategy = data["armies_strategy"]
    squads_per_army = data["squads_per_army"]
    units_per_squad = data["units_per_squad"]
    seed = Random(data["seed"])
    specific_army_number = data["specific_army_number"]

    armies = [
        UnitsBuilder(
            strategy, squads_per_army, units_per_squad, seed, all_strategies
        ).create_army(f"ARMY_{army+1}")
        for army in range(armies_num)
    ]

    armies[specific_army_number - 1].strategy = data["specific_army_strategy"]
    game = Game(armies, seed)
    game.run_game()


if __name__ == "__main__":
    main()
