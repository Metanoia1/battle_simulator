"""Test for Soldier class from units.py module

Command line: python -m pytest tests/test_soldier_class.py
"""
# pylint: disable=(missing-function-docstring)


def test_soldier_instance_creation(soldier, soldier_values):
    for attr_name in soldier_values:
        assert getattr(soldier, attr_name) is soldier_values.get(attr_name)


def test_soldier_is_active_property(soldier):
    assert getattr(soldier, "is_active") is True
    soldier.get_damage(99)
    assert getattr(soldier, "is_active") is True
    soldier.get_damage(1)
    assert getattr(soldier, "is_active") is False


def test_soldier_is_ready_method(soldier):
    assert soldier.is_ready(0) is False
    assert soldier.is_ready(99) is False
    assert soldier.is_ready(100) is True
    soldier.last_attack = 1
    assert soldier.is_ready(100) is False


def test_soldier_success_property(soldier):
    soldier.experience = 50
    assert soldier.success ==  1.0


def test_soldier_attack_method(soldier):
    soldier.experience = 50
    assert soldier.attack(100) == 0.55
    assert soldier.is_ready(199) is False
    assert soldier.is_ready(200) is True


def test_soldier_get_damage_method(soldier):
    soldier.get_damage(0.55)
    assert getattr(soldier, "health") == 99.45
    assert getattr(soldier, "is_active") is True
    soldier.get_damage(99.45)
    assert getattr(soldier, "health") == 0
    assert getattr(soldier, "is_active") is False
