import json


def get_data_from_json_file(filename):
    with open(filename) as json_file:
        file_ = json.load(json_file)
    return file_


def clear_log():
    with open("log.txt", "w") as log:
        log.write("")


def mylogger(attacking_army, defending_army):
    with open("log.txt", "a") as log:
        log.write(f"{attacking_army}-{attacking_army.strategy} VS ")
        log.write(f"{defending_army}\n")
