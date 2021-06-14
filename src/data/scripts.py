"""
Module contains scripts used to load/save data from/to files during game.

"""


import json
import os
from json.decoder import JSONDecodeError
from pygame import display
from datetime import datetime

from .languages.texts import TEXTS


def _max_available_resolution():
    """Returns maximum screen resolution suggested by pygame.
    This resolution is supposed to be the screen size of the monitor.
    """
    display.init()
    return list(display.list_modes()[0])


def _validate_config():
    """Check if file 'config.json' exists and stores valid data.
    If not, writes valid default data to the file.
    """
    def is_valid(data) -> bool:
        return (type(data) == dict and
                "save" in data and data["save"] in ("empty", "save_1", "save_2", "save_3") and
                "language" in data and data["language"] in LANGUAGES and
                "resolution" in data and data["resolution"] in SUPPORTED_RESOLUTIONS)

    def write_default_data():
        with open(_CONFIG_FILE, "w", encoding='utf-8') as f:
            data = {"language": LANGUAGES[0], "resolution": [1024, 768], "save": "empty"}
            json.dump(data, f)

    try:
        with open(_CONFIG_FILE, "r+", encoding='utf-8') as file:
            try:
                data = json.load(file)
            except JSONDecodeError:
                write_default_data()
            else:
                if not is_valid(data):
                    write_default_data()
    except (IOError, FileNotFoundError):
        write_default_data()


def load_config():
    _validate_config()
    with open(_CONFIG_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_resolution():
    return load_config()["resolution"]


def load_language():
    return LANGUAGES.index(load_config()["language"])


def load_current_save():
    return load_config()["save"]


def update_config_file(resolution=None, language=None, save=None):
    _validate_config()
    with open(_CONFIG_FILE, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        if resolution is not None:
            data["resolution"] = resolution
        if language is not None:
            data["language"] = language
        if save is not None:
            data["save"] = save
        file.seek(0)
        file.truncate(0)
        json.dump(data, file, ensure_ascii=False, indent=4)


def update_save_file(save_name,
                     tank, tanks_history, health,
                     enemies_killed, bubbles_collected,
                     visited_rooms, enemies_dict, current_room,
                     boss_generated, boss_disposition, boss_position,
                     hints_history):
    """Update data of save file with given name. """
    if save_name is None:
        return
    data = {
        "tank": list(tank),
        "tanks history": [list(tank) for tank in tanks_history],
        "health": health,
        "enemies killed": enemies_killed,
        "bubbles collected": bubbles_collected,
        "visited rooms": {"%d %d" % room: [list(neighbour) for neighbour in neighbours]
                          for room, neighbours in visited_rooms.items()},
        "enemies": {"%d %d" % room: dict(enemies) for room, enemies in enemies_dict.items()},
        "current room": list(current_room),
        "boss generated": boss_generated,
        "boss disposition": boss_disposition,
        "boss position": None if boss_position is None else list(boss_position),
        "hints history": {"%d %d" % room: hint for room, hint in hints_history.items()},
        "time": datetime.today().isoformat(sep=' ', timespec='minutes')
    }
    file_path = os.path.join(_USER_DIR, "%s.json" % save_name)
    with open(file_path, 'w') as file:
        json.dump(data, file)


def create_save_file(save_name):
    """Created new save file with given name and
    default data in user directory.
    """
    data = {
        "tank": [0, 0],
        "tanks history": [[0, 0]],
        "health": 0,
        "enemies killed": "0",
        "bubbles collected": "0",
        "visited rooms": {"0 0": []},
        "enemies": {"0 0": {}},
        "current room": [0, 0],
        "boss generated": False,
        "boss killed": False,
        "boss position": None,
        "boss disposition": 0,
        "hints history": {"0 0": 0},
        "time": datetime.today().isoformat(sep=' ', timespec='minutes')
    }
    file_path = os.path.join(_USER_DIR, "%s.json" % save_name)
    with open(file_path, 'w') as file:
        json.dump(data, file)


def delete_save_file(name):
    """Deletes save file with given name from user directory. """
    file_path = os.path.join(_USER_DIR, "%s.json" % name)
    os.remove(file_path)


def load_save_file(save_name: str):
    file_path = os.path.join(_USER_DIR, "%s.json" % save_name)
    try:
        file = open(file_path, 'r')
    except (IOError, FileNotFoundError):
        return None
    return json.load(file)


# Make sure that the directory for config file exists
_USER_DIR = os.path.join(os.path.abspath(os.path.expanduser("~")), f".Underwater_Battles")
if not os.path.exists(_USER_DIR):
    os.mkdir(_USER_DIR)

_CONFIG_FILE = os.path.join(_USER_DIR, 'config.json')


# Find out what game resolutions are supported by computer
default_resolutions = [
    [800, 600],
    [1024, 768],
    [1152, 864],
    [1280, 720],
    [1280, 960],
    [1366, 768],
    [1400, 1050],
    [1440, 900],
    [1600, 900],
    [1680, 1080],
    [1920, 1080]
]
max_res = _max_available_resolution()
SUPPORTED_RESOLUTIONS = [res for res in default_resolutions if res < max_res] + [max_res]
LANGUAGES = TEXTS["language"]


__all__ = [

    "SUPPORTED_RESOLUTIONS",
    "load_resolution",
    "load_language",
    "load_current_save",
    "load_save_file",
    "create_save_file",
    "update_save_file",
    "delete_save_file",
    "update_config_file"

]
