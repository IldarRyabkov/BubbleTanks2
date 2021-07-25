"""
Module contains scripts used to load/save data from/to files during game.

"""

import json
import os
from json.decoder import JSONDecodeError
import pygame as pg
from datetime import datetime
import hashlib

from data.languages import TEXTS


def _max_available_resolution():
    """Returns maximum screen resolution suggested by pygame.
    This resolution is supposed to be the screen size of the monitor.
    """
    pg.display.init()
    return list(pg.display.list_modes()[0])


def _validate_config():
    """Check if file 'config.json' exists and stores valid data.
    If not, writes valid default data to the file.
    """
    def is_valid(data) -> bool:
        if type(data) is not dict:
            return False
        if "screen mode" not in data or data["screen mode"] not in [0, 1, 2]:
            return False
        if "save" not in data:
            return False
        if data["save"] in ("save_1", "save_2", "save_3"):
            save_file = os.path.join(_USER_DIR, "%s.json" % data["save"])
            if not os.path.isfile(save_file):
                return False
        if data["save"] not in ("empty", "save_1", "save_2", "save_3"):
            return False
        if "language" not in data or data["language"] not in LANGUAGES:
            return False
        if "resolution" not in data or data["resolution"] not in SUPPORTED_RESOLUTIONS:
            return False
        if "controls" not in data or type(data["controls"]) != dict:
            return False
        if not all(k in ("up", "down", "left", "right", "superpower", "pause")
                   for k in data["controls"]):
            return False
        for key_name in data["controls"].values():
            try:
                pg.key.key_code(key_name)
            except ValueError:
                return False
        return True

    def write_default_data():
        with open(_CONFIG_FILE, "w", encoding='utf-8') as f:
            data = {
                "screen mode": 1,
                "language": LANGUAGES[0],
                "resolution": [1024, 768],
                "save": "empty",
                "controls": {
                    "up": "w",
                    "down": "s",
                    "left": "a",
                    "right": "d",
                    "superpower": "space",
                    "pause": "p"
                }
            }
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


def _is_valid_save_data(save_data):
    if type(save_data) is not dict or "magic number" not in save_data:
        return False
    raw_data = {k: v for k, v in save_data.items() if k != "magic number"}
    magic_number = int(hashlib.sha512(json.dumps(raw_data).encode()).hexdigest(), 16)
    return magic_number == save_data["magic number"]


def load_config():
    _validate_config()
    with open(_CONFIG_FILE, 'r', encoding='utf-8') as file:
        return json.load(file)


def load_resolution():
    return load_config()["resolution"]


def load_language():
    return LANGUAGES.index(load_config()["language"])


def load_screen_mode():
    return load_config()["screen mode"]


def load_current_save():
    return load_config()["save"]


def load_controls():
    controls = load_config()["controls"]
    for control, key_name in controls.items():
        controls[control] = pg.key.key_code(key_name)
    return controls


def update_config_file(resolution=None, language=None, save=None, screen_mode=None, controls=None):
    _validate_config()
    with open(_CONFIG_FILE, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        if resolution is not None:
            data["resolution"] = resolution
        if language is not None:
            data["language"] = language
        if save is not None:
            data["save"] = save
        if screen_mode is not None:
            data["screen mode"] = screen_mode
        if controls is not None:
            data["controls"] = {k: pg.key.name(v) for k, v in controls.items()}
        file.seek(0)
        file.truncate(0)
        json.dump(data, file, ensure_ascii=False, indent=4)


def update_save_file(save_name,
                     tank, tanks_history, health, max_cumulative_health,
                     enemies_killed, bubbles_collected,
                     visited_rooms, enemies_dict, current_room,
                     boss_generated, boss_position,
                     hints_history):
    """Update data of save file with given name. """
    data = {
        "tank": tank,
        "tanks history": tanks_history,
        "health": health,
        "max cumulative health": max_cumulative_health,
        "enemies killed": enemies_killed,
        "bubbles collected": bubbles_collected,
        "visited rooms": {"%d %d" % room: [neighbour for neighbour in neighbours]
                          for room, neighbours in visited_rooms.items()},
        "enemies": {"%d %d" % room: dict(enemies) for room, enemies in enemies_dict.items()},
        "current room": current_room,
        "boss generated": boss_generated,
        "boss position": None if boss_position is None else boss_position,
        "hints history": {"%d %d" % room: hint for room, hint in hints_history.items()},
        "time": datetime.today().isoformat(sep=' ', timespec='minutes')
    }
    magic_number = int(hashlib.sha512(json.dumps(data).encode()).hexdigest(), 16)
    data["magic number"] = magic_number
    file_path = os.path.join(_USER_DIR, "%s.json" % save_name)
    with open(file_path, 'w') as file:
        json.dump(data, file)


def create_save_file(save_name):
    """Created new save file with given name and
    default data in user directory.
    """
    data = {
        "tank": (0, 0),
        "tanks history": ((0, 0),),
        "health": 0,
        "max cumulative health": 0,
        "enemies killed": "0",
        "bubbles collected": "0",
        "visited rooms": {"0 0": ()},
        "enemies": {"0 0": {}},
        "current room": (0, 0),
        "boss generated": False,
        "boss position": None,
        "hints history": {"0 0": 0},
        "time": datetime.today().isoformat(sep=' ', timespec='minutes')
    }
    magic_number = int(hashlib.sha512(json.dumps(data).encode()).hexdigest(), 16)
    data["magic number"] = magic_number
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
    try:
        data = json.load(file)
    except JSONDecodeError:
        return None
    if not _is_valid_save_data(data):
        return None
    if "max cumulative health" not in data:
        data["max cumulative health"] = 0
    return data


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
SUPPORTED_RESOLUTIONS = [res for res in default_resolutions if res <= max_res]
LANGUAGES = TEXTS["language"]


__all__ = [

    "SUPPORTED_RESOLUTIONS",
    "load_resolution",
    "load_language",
    "load_screen_mode",
    "load_current_save",
    "load_controls",
    "load_save_file",
    "create_save_file",
    "update_save_file",
    "delete_save_file",
    "update_config_file"

]
