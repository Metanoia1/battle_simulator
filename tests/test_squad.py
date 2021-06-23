"""Test for squad.py module

Command line: python -m pytest tests/test_squad.py
"""
from random import Random

import pytest

from strategies import all_strategies
from units import Soldier, Vehicle
from squad import Squad


SEED = 12345


@pytest.fixture
def squad_values():
    return {
        "units": [
            Soldier(Random(SEED)),
            Soldier(Random(SEED)),
            Soldier(Random(SEED)),
            Vehicle(
                [
                    Soldier(Random(SEED)),
                    Soldier(Random(SEED)),
                    Soldier(Random(SEED)),
                ],
                Random(SEED),
            ),
            Vehicle(
                [
                    Soldier(Random(SEED)),
                    Soldier(Random(SEED)),
                    Soldier(Random(SEED)),
                ],
                Random(SEED),
            ),
        ],
        "strategy": "strongest",
        "strategies": all_strategies,
    }


@pytest.fixture
def squad(squad_values):
    return Squad(**squad_values)


def test_squad_instance_creation(squad, squad_values):
    for attr_name in squad_values:
        assert getattr(squad, attr_name) == squad_values.get(attr_name)


def test_squad_is_active_property(squad):
    assert getattr(squad, "is_active") == True
    for u in squad.units:
        u._health = 0
    assert getattr(squad, "is_active") == False
    squad.units[0]._health = 0.5
    assert getattr(squad, "is_active") == True


def test_squad_is_ready_method(squad):
    assert squad.is_ready(0) == False
    assert squad.is_ready(1001) == True


def test_squad_success_property(squad):
    for u in squad.units:
        if isinstance(u, Soldier):
            u.experience = 50
        if isinstance(u, Vehicle):
            for o in u.operators:
                o.experience = 50
    assert squad.success == 1.0


def test_squad_attack_method(squad):
    for u in squad.units:
        if isinstance(u, Soldier):
            u.experience = 50
        if isinstance(u, Vehicle):
            for o in u.operators:
                o.experience = 50
    assert squad.attack(1001) == 4.85


def test_squad_get_damage_method(squad):
    squad.get_damage(500)
    assert getattr(squad.units[0], "health") == 0
    assert getattr(squad.units[1], "health") == 0
    assert getattr(squad.units[2], "health") == 0
    assert getattr(squad.units[3], "health") == 40
    assert sum(o.health for o in squad.units[3].operators) == 260
    assert getattr(squad.units[4], "health") == 40
    assert sum(o.health for o in squad.units[4].operators) == 260
