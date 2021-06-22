"""Test for units.py module

Command line: python -m pytest tests/test_units.py
"""
from random import Random

import pytest

from units import Unit, Soldier, Vehicle


SEED = 12345

# Test Soldier
###############################################################################
@pytest.fixture
def soldier_values():
    return {
        "name": "soldier",
        "random_": Random(SEED),
        "health": 100,
        "recharge": 100,
        "experience": 16,
    }


@pytest.fixture
def soldier(soldier_values):
    return Soldier(**soldier_values)


def test_soldier_instance_creation(soldier, soldier_values):
    for attr_name in soldier_values:
        assert getattr(soldier, attr_name) == soldier_values.get(attr_name)


def test_soldier_is_active_property(soldier):
    assert getattr(soldier, "is_active") == True
    soldier.health = 0
    assert getattr(soldier, "is_active") == False


def test_soldier_is_ready_method(soldier):
    assert soldier.is_ready(0) == False
    assert soldier.is_ready(99) == False
    assert soldier.is_ready(100) == True
    soldier.last_attack = 1
    assert soldier.is_ready(100) == False


def test_soldier_success_property(soldier):
    soldier.experience = 50
    assert soldier.success == 1.0


def test_soldier_attack_method(soldier):
    soldier.experience = 50
    assert soldier.attack(100) == 0.55
    assert soldier.is_ready(155) == False
    assert soldier.is_ready(200) == True


def test_soldier_get_damage_method(soldier):
    soldier.get_damage(0.55)
    assert getattr(soldier, "health") == 99.45
    assert getattr(soldier, "is_active") == True
    soldier.get_damage(100)
    assert getattr(soldier, "health") == 0
    assert getattr(soldier, "is_active") == False


# Test Vehicle
###############################################################################
@pytest.fixture
def vehicle_values(soldier):
    return {
        "operators": [
            Soldier("soldier_1", Random(SEED)),
            Soldier("soldier_2", Random(SEED)),
            Soldier("soldier_3", Random(SEED)),
        ],
        "name": "vehicle",
        "random_": Random(SEED),
        "health": 100,
        "recharge": 1001,
    }


@pytest.fixture
def vehicle(vehicle_values):
    return Vehicle(**vehicle_values)


def test_vehicle_operators_is_the_diff_instances(vehicle):
    assert len(set(vehicle.operators)) == 3


def test_vehicle_instance_creation(vehicle, vehicle_values):
    for attr_name in vehicle_values:
        assert getattr(vehicle, attr_name) == vehicle_values.get(attr_name)


def test_vehicle_is_active_property(vehicle, vehicle_values):
    assert getattr(vehicle, "is_active") == True
    vehicle.health = 0
    assert getattr(vehicle, "is_active") == False
    vehicle.health = 1
    assert getattr(vehicle, "is_active") == True
    for operator in vehicle.operators:
        operator.health = 0
    vehicle.health = 1000
    assert getattr(vehicle, "health") == vehicle_values.get("health")
    assert getattr(vehicle, "is_active") == False


def test_vehicle_is_ready_method(vehicle, vehicle_values):
    assert vehicle.is_ready(0) == False
    assert vehicle.is_ready(vehicle_values["recharge"] - 1) == False
    assert vehicle.is_ready(vehicle_values["recharge"]) == True
    vehicle.last_attack = 1
    assert vehicle.is_ready(vehicle_values["recharge"]) == False


def test_vehicle_success_property(vehicle):
    for o in vehicle.operators:
        o.experience = 50
    assert vehicle.success == 1.0


def test_vehicle_attack_method(vehicle, vehicle_values):
    for o in vehicle.operators:
        o.experience = 50
    assert vehicle.attack(100) == 1.6
    assert vehicle.is_ready(vehicle_values["recharge"] + 99) == False
    assert vehicle.is_ready(vehicle_values["recharge"] + 100) == True


def test_vehicle_get_damage_method(vehicle):
    vehicle.get_damage(100)
    assert vehicle.health == 40
    assert vehicle.operators[0].health == 90
    assert vehicle.operators[1].health == 80
    assert vehicle.operators[2].health == 90
    vehicle.health = 1000
    vehicle.get_damage(10)
    assert getattr(vehicle, "health") == 94
    assert getattr(vehicle, "is_active") == True
    vehicle.get_damage(157)
    assert getattr(vehicle, "is_active") == False
    vehicle.health = 100
    assert getattr(vehicle, "is_active") == True
    for o in vehicle.operators:
        o.health = 0
    assert getattr(vehicle, "is_active") == False
