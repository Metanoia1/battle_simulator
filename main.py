"""Module to start the game"""
from random import Random

from game import Game
from strategies import all_strategies
from units_builder import UnitsBuilder
from utils import clear_log, get_data_from_json_file


def main():
    """This function creates and starts the game"""
    clear_log()

    data = get_data_from_json_file("config.json")
    armies_num = data["number_of_armies"]
    squads_per_army = data["squads_per_army"]
    units_per_squad = data["units_per_squad"]
    seed = Random(data["seed"])
    strategies = data["strategies"]

    armies = [
        UnitsBuilder(
            strategies[army],
            all_strategies,
            squads_per_army,
            units_per_squad,
            seed,
        ).create_army(f"ARMY_{army+1}")
        for army in range(armies_num)
    ]

    game = Game(armies)
    game.run_game()


if __name__ == "__main__":
    main()
