"""
Test for army.py module
Command line: python -m pytest tests/test_army.py
"""
from time import sleep

import pytest

from units import Soldier, Vehicle
from squad import Squad
from army import Army


@pytest.fixture
def army_values():
    return {
        "name": "armySSS",
        "squads": {
            Squad("", {Soldier(), Soldier(), Soldier(), Soldier(), Soldier()}),
            Squad("", {Soldier(), Soldier(), Soldier(), Soldier(), Soldier()}),
        },
    }


@pytest.fixture
def army(army_values):
    return Army(**army_values)


def test_create(army, army_values):
    for attr_name in army_values:
        assert getattr(army, attr_name) == army_values.get(attr_name)


@pytest.mark.parametrize(
    "squads, ex",
    [
        ("a", TypeError),
        ([], TypeError),
        (10000.0004, TypeError),
        ({}, TypeError),
        ({Soldier(), Soldier(), 35}, TypeError),
        ({1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, TypeError),
        ({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, TypeError),
        ({Soldier(), Soldier(), Soldier(), Soldier()}, TypeError),
    ],
)
def test_invalid_squads(squads, ex, army_values):
    army_values["squads"] = squads
    with pytest.raises(ex):
        Army(**army_values)


@pytest.mark.parametrize(
    "name, ex",
    [
        ("a", ValueError),
        ("asdfkjasldkfjasldfkjaslkdfja", ValueError),
        ("          ", ValueError),
        ([], TypeError),
        (10000.0004, TypeError),
        ({}, TypeError),
        ({Soldier(), Soldier(), 35}, TypeError),
        ({1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, TypeError),
        ({1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}, TypeError),
        ({Soldier(), Soldier(), Soldier(), Soldier()}, TypeError),
    ],
)
def test_invalid_name(name, ex, army_values):
    army_values["name"] = name
    with pytest.raises(ex):
        Army(**army_values)
