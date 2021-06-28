"""Test for Army class from army.py module

Command line: python -m pytest tests/test_army_class.py
"""
# pylint: disable=(missing-function-docstring)


def test_army_instance_creation(army, army_values):
    for attr_name in army_values:
        assert getattr(army, attr_name) is army_values.get(attr_name)


def test_army_health_line_property(army):
    assert army.health_line == 50 * "."
    army.get_damage(577)
    assert army.health_line == 25 * "."


def test_army_repr(army):
    assert repr(army) == f"{army.name} health: {int(army.health)}"
    army.get_damage(1664.99)
    assert repr(army) == f"{army.name} health: {army.health}"
