"""
Module to start the game
"""
from game import Game
from units_builder import UnitsBuilder


def main():
    armies = {UnitsBuilder(f"ARMIE_{army+1}", 5, 2)() for army in range(5)}
    game = Game(armies)
    game.run_game()


if __name__ == "__main__":
    main()
