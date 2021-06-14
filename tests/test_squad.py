"""
Test for squad.py module
Command line: python -m pytest tests/test_squad.py
"""
from time import sleep

import pytest

from units import Soldier, Vehicle
from squad import Squad


@pytest.fixture
def squad_values():
    return {
        "strategy": "weakest",
        "units": {
            Vehicle({Soldier()}),
            Vehicle({Soldier()}),
            Soldier(),
            Soldier(),
            Vehicle({Soldier()}),
        },
    }


@pytest.fixture
def squad(squad_values):
    return Squad(**squad_values)


def test_create(squad, squad_values):
    for attr_name in squad_values:
        assert getattr(squad, attr_name) == squad_values.get(attr_name)


@pytest.mark.parametrize(
    "units, ex",
    [
        ("a", TypeError),
        ([], TypeError),
        (10000.0004, TypeError),
        ({}, TypeError),
        ({Soldier(), Soldier(), 35}, ValueError),
        ({1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, TypeError),
        ({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, ValueError),
        ({Soldier(), Soldier(), Soldier(), Soldier()}, ValueError),
    ],
)
def test_invalid_operators(units, ex, squad_values):
    squad_values["units"] = units
    with pytest.raises(ex):
        Squad(**squad_values)


def test_strategy(squad):
    squad.strategy = 1
    assert getattr(squad, "strategy") == "random"
    squad.strategy = "weakest"
    assert getattr(squad, "strategy") == "weakest"
    squad.strategy = "strongest"
    assert getattr(squad, "strategy") == "strongest"
