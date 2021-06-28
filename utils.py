"""Different utils for the battle simulator"""
import json
from typing import Dict
from army import Army


def get_data_from_json_file(filename: str) -> Dict:
    """Turns JSON file into python dict"""
    with open(filename) as json_file:
        file_ = json.load(json_file)
    return file_


def clear_log() -> None:
    """Just clears the logs.log file"""
    with open("logs.log", "w") as log:
        log.write("")


def mylogger(attacking_army: Army, defending_army: Army) -> None:
    """Writes some logs to logs.log file"""
    with open("logs.log", "a") as log:
        log.write(f"{attacking_army}-{attacking_army.strategy} VS ")
        log.write(f"{defending_army}\n")
