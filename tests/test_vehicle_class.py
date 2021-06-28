"""Test for Vehicle class from units.py module

Command line: python -m pytest tests/test_vehicle_class.py
"""
# pylint: disable=(missing-function-docstring)
import pytest


def test_vehicle_instance_creation(vehicle, vehicle_values):
    for attr_name in vehicle_values:
        assert getattr(vehicle, attr_name) is vehicle_values.get(attr_name)


def test_vehicle_is_active_property(vehicle):
    assert vehicle.is_active is True
    vehicle.operators[0].get_damage(100)
    vehicle.operators[1].get_damage(100)
    vehicle.operators[2].get_damage(100)
    assert vehicle.is_active is False


def test_vehicle_is_ready_method(vehicle, vehicle_values):
    assert vehicle.is_ready(0) is False
    assert vehicle.is_ready(vehicle_values["recharge"] - 1) is False
    assert vehicle.is_ready(vehicle_values["recharge"]) is True
    vehicle.last_attack = 1
    assert vehicle.is_ready(vehicle_values["recharge"]) is False


@pytest.mark.parametrize(
    "index, result",
    [
        (0, 50),
        (1, 50),
        (2, 50),
    ],
)
def test_vehicle_success_property(vehicle, index, result):
    assert vehicle.operators[index].experience == result
    assert vehicle.success == 1.0


def test_vehicle_attack_method(vehicle, vehicle_values):
    assert vehicle.attack(100) == 1.6
    assert vehicle.is_ready(vehicle_values["recharge"] + 99) is False
    assert vehicle.is_ready(vehicle_values["recharge"] + 100) is True


def test_vehicle_get_damage_method(vehicle):
    assert vehicle.health == 100
    assert vehicle.operators[0].health == 100
    assert vehicle.operators[1].health == 100
    assert vehicle.operators[2].health == 100
    vehicle.get_damage(100)
    assert vehicle.health == 40
    assert vehicle.operators[0].health == 90
    assert vehicle.operators[1].health == 80
    assert vehicle.operators[2].health == 90
    vehicle.operators[0].get_damage(90)
    assert vehicle.operators[0].health == 0
    vehicle.operators[1].get_damage(80)
    assert vehicle.operators[1].health == 0
    vehicle.operators[2].get_damage(90)
    assert vehicle.operators[2].health == 0
    assert vehicle.is_active is False
    assert vehicle.health == 40
    vehicle.get_damage(100)
    assert vehicle.health == 0
