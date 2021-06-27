"""Creating instances for testing"""
# pylint: disable=(missing-function-docstring)
# pylint: disable=(redefined-outer-name)
from random import Random

import pytest

from strategies import all_strategies
from units import Soldier, Vehicle
from squad import Squad


SEED = 12345


@pytest.fixture
def soldier_values():
    return {
        "random_": Random(SEED),
        "health": 100,
        "recharge": 100,
        "experience": 16,
    }


@pytest.fixture
def vehicle_values():
    return {
        "operators": [
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
        ],
        "random_": Random(SEED),
        "health": 100,
        "recharge": 1001,
    }


@pytest.fixture
def squad_values():
    return {
        "units": [
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
            Vehicle(
                [
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                ],
                Random(SEED),
            ),
            Vehicle(
                [
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                ],
                Random(SEED),
            ),
        ],
        "strategy": "strongest",
        "strategies": all_strategies,
    }


@pytest.fixture
def squad1_values():
    return {
        "units": [
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
            Vehicle(
                [
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                ],
                Random(SEED),
            ),
            Vehicle(
                [
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                ],
                Random(SEED),
            ),
        ],
        "strategy": "strongest",
        "strategies": all_strategies,
    }


@pytest.fixture
def squad2_values():
    return {
        "units": [
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
            Vehicle(
                [
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                ],
                Random(SEED),
            ),
            Vehicle(
                [
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                ],
                Random(SEED),
            ),
        ],
        "strategy": "strongest",
        "strategies": all_strategies,
    }


@pytest.fixture
def squad3_values():
    return {
        "units": [
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
            Soldier(Random(SEED), experience=50),
            Vehicle(
                [
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                ],
                Random(SEED),
            ),
            Vehicle(
                [
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                    Soldier(Random(SEED), experience=50),
                ],
                Random(SEED),
            ),
        ],
        "strategy": "strongest",
        "strategies": all_strategies,
    }


@pytest.fixture
def soldier(soldier_values):
    return Soldier(**soldier_values)


@pytest.fixture
def vehicle(vehicle_values):
    return Vehicle(**vehicle_values)


@pytest.fixture
def squad(squad_values):
    return Squad(**squad_values)


@pytest.fixture
def squad1(squad1_values):
    return Squad(**squad1_values)


@pytest.fixture
def squad2(squad2_values):
    return Squad(**squad2_values)


@pytest.fixture
def squad3(squad3_values):
    return Squad(**squad3_values)
