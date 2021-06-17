from random import Random


def get_weakest(squads):
    return sorted(squads, key=lambda squad: squad.health)[0]


def get_strongest(squads):
    return sorted(squads, key=lambda squad: squad.health, reverse=True)[0]


def get_random(squads):
    _random = Random(12345)
    return _random.choice(squads)
