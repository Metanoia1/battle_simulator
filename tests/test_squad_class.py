"""Test for Squad class from squad.py module

Command line: python -m pytest tests/test_squad_class.py
"""
# pylint: disable=(missing-function-docstring)


def test_squad_instance_creation(squad, squad_values):
    for attr_name in squad_values:
        assert getattr(squad, attr_name) is squad_values.get(attr_name)


def test_squad_health_property(squad):
    health = sum(u.health for u in squad.units if u.is_active)
    assert getattr(squad, "health") == health


def test_squad_is_active_property(squad):
    assert getattr(squad, "is_active") is True
    squad.get_damage(834)
    assert getattr(squad, "is_active") is False


def test_squad_success_property(squad):
    assert squad.success == 1.0


def test_squad_attack_method(squad):
    assert squad.attack(1001) == 4.85


def test_squad_get_damage_method(squad):
    squad.get_damage(500)
    assert getattr(squad.units[0], "health") == 0
    assert getattr(squad.units[1], "health") == 0
    assert getattr(squad.units[2], "health") == 0
    assert getattr(squad.units[3], "health") == 40
    assert getattr(squad.units[4], "health") == 40
    assert sum(o.health for o in squad.units[3].operators) == 260
    assert sum(o.health for o in squad.units[4].operators) == 260


def test_squads_is_the_diff_instances(squad1, squad2, squad3):
    squads = [squad1, squad2, squad3]
    assert len(set(squads)) == 3


def test_get_defending_method(squad, squad1, squad2, squad3):
    squads = [squad1, squad2, squad3]
    squad.strategy = "weakest"
    squad2.get_damage(1)
    assert squad.get_defending(squads) is squad2
    squad.strategy = "strongest"
    squad1.get_damage(1)
    assert squad.get_defending(squads) is squad3
    squad.strategy = "random"
    assert squad.get_defending(squads) is squad2
