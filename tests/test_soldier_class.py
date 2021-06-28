"""Test for Soldier class from units.py module

Command line: python -m pytest tests/test_soldier_class.py
"""
# pylint: disable=(missing-function-docstring)
import pytest


def test_soldier_instance_creation(soldier, soldier_values):
    for attr_name in soldier_values:
        assert getattr(soldier, attr_name) is soldier_values.get(attr_name)


@pytest.mark.parametrize(
    "value, ex",
    [
        ([1, 2, 3], TypeError),
        ("hello", TypeError),
        ({"a": 7}, TypeError),
    ],
)
def test_soldier_invalid_last_attack(soldier, value, ex):
    with pytest.raises(ex):
        soldier.last_attack = value


@pytest.mark.parametrize(
    "value, ex",
    [
        ([1, 2, 3], TypeError),
        ("hello", TypeError),
        ({"a": 7}, TypeError),
        (2.2, TypeError),
    ],
)
def test_soldier_experience_property(soldier, value, ex):
    with pytest.raises(ex):
        soldier.experience = value
    soldier.experience = 100
    assert soldier.experience == 50
    soldier.experience = -10
    assert soldier.experience == 0


def test_soldier_is_active_property(soldier):
    assert soldier.is_active is True
    soldier.get_damage(99)
    assert soldier.is_active is True
    soldier.get_damage(1)
    assert soldier.is_active is False


def test_soldier_is_ready_method(soldier):
    assert soldier.is_ready(0) is False
    assert soldier.is_ready(99) is False
    assert soldier.is_ready(100) is True
    soldier.last_attack = 1
    assert soldier.is_ready(100) is False


def test_soldier_success_property(soldier):
    soldier.experience = 50
    assert soldier.success == 1.0


def test_soldier_attack_method(soldier):
    soldier.experience = 50
    assert soldier.attack(100) == 0.55
    assert soldier.is_ready(199) is False
    assert soldier.is_ready(200) is True


def test_soldier_get_damage_method(soldier):
    soldier.get_damage(0.55)
    assert soldier.health == 99.45
    assert soldier.is_active is True
    soldier.get_damage(99.45)
    assert soldier.health == 0
    assert soldier.is_active is False
