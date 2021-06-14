"""
Test for units.py module
Command line: python -m pytest tests/test_units.py
"""
from time import sleep

import pytest

from units import Unit, Soldier, Vehicle


###############################################################################
# class Unit


@pytest.fixture
def unit_values():
    return {
        "health": 100,
        "recharge": 100,
    }


@pytest.fixture
def unit(unit_values):
    return Unit(**unit_values)


def test_create(unit, unit_values):
    for attr_name in unit_values:
        assert getattr(unit, attr_name) == unit_values.get(attr_name)


@pytest.mark.parametrize(
    "health, ex",
    [
        ("a", TypeError),
        ([], TypeError),
        (10001, ValueError),
        (10000.0004, ValueError),
    ],
)
def test_invalid_unit_health(health, ex, unit_values):
    unit_values["health"] = health
    with pytest.raises(ex):
        Unit(**unit_values)


@pytest.mark.parametrize(
    "recharge, ex",
    [
        ("a", TypeError),
        (55.5, TypeError),
        (2001, ValueError),
        (99, ValueError),
    ],
)
def test_invalid_unit_recharge(recharge, ex, unit_values):
    unit_values["recharge"] = recharge
    with pytest.raises(ex):
        Unit(**unit_values)


def test_is_active(unit):
    unit.health = 1
    assert getattr(unit, "is_active") == True
    unit.health = -1
    assert getattr(unit, "is_active") == False


###############################################################################
# class Soldier


@pytest.fixture
def soldier_values():
    return {
        "experience": 25,
    }


@pytest.fixture
def soldier(soldier_values):
    return Soldier(**soldier_values)


def test_create(soldier, soldier_values):
    for attr_name in soldier_values:
        assert getattr(soldier, attr_name) == soldier_values.get(attr_name)


@pytest.mark.parametrize(
    "experience, ex",
    [
        ("a", TypeError),
        ([], TypeError),
        (10000.0004, TypeError),
    ],
)
def test_invalid_soldier_experience(experience, ex, soldier_values):
    soldier_values["experience"] = experience
    with pytest.raises(ex):
        Soldier(**unit_values)


def test_experience_setter(soldier, soldier_values):
    soldier.experience = 0
    assert getattr(soldier, "experience") == 0
    soldier.experience = 51
    assert getattr(soldier, "experience") == 50
    soldier.experience = -1000
    assert getattr(soldier, "experience") == 0
    soldier.experience = 0
    soldier.attack()
    assert getattr(soldier, "experience") == 1
    with pytest.raises(TypeError):
        soldier.experience = "asldkf"
    with pytest.raises(TypeError):
        soldier.experience = 7.77


def test_attack(soldier, soldier_values):
    soldier.attack()
    assert getattr(soldier, "is_ready") == False
    sleep(0.1)
    assert getattr(soldier, "is_ready") == True


###############################################################################
# class Vehicle


@pytest.fixture
def vehicle_values():
    return {
        "operators": {Soldier(), Soldier(), Soldier()},
    }


@pytest.fixture
def vehicle(vehicle_values):
    return Vehicle(**vehicle_values)


def test_create(vehicle, vehicle_values):
    for attr_name in vehicle_values:
        assert getattr(vehicle, attr_name) == vehicle_values.get(attr_name)


def test_operators_len(vehicle):
    lenght = len(vehicle.operators)
    assert lenght == 3


@pytest.mark.parametrize(
    "operators, ex",
    [
        ("a", TypeError),
        ([], TypeError),
        (10000.0004, TypeError),
        ({}, TypeError),
        ({Soldier(), Soldier(), 35}, TypeError),
        ({Soldier(), Soldier(), Soldier(), Soldier()}, ValueError),
    ],
)
def test_invalid_operators(operators, ex, vehicle_values):
    vehicle_values["operators"] = operators
    with pytest.raises(ex):
        Vehicle(**vehicle_values)
