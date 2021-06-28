"""Strategies (dict) implementation module"""
# pylint: disable=(missing-class-docstring)
# pylint: disable=(too-few-public-methods)
# pylint: disable=(missing-function-docstring)
from random import Random
from typing import Dict, List, Protocol

from units import Unit
from utils import get_data_from_json_file


class Strategy(Protocol):
    def __call__(self, units: List[Unit]) -> Unit:
        pass


def get_weakest(units: List[Unit]) -> Unit:
    return sorted(units, key=lambda unit: unit.health)[0]


def get_strongest(units: List[Unit]) -> Unit:
    return sorted(units, key=lambda unit: unit.health, reverse=True)[0]


class RandomStrategy:
    def __init__(self, random: Random) -> None:
        self.random = random

    def __call__(self, units: List[Unit]) -> Unit:
        return self.random.choice(units)


seed = get_data_from_json_file("config.json")["seed"]

all_strategies: Dict[str, Strategy] = {
    "weakest": get_weakest,
    "strongest": get_strongest,
    "random": RandomStrategy(Random(seed)),
}
