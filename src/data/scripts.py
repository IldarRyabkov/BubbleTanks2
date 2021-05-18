"""
Module contains scripts used to load data from 'config.json'
and save data to 'config.json' during game.

"""


import json
import os
from json.decoder import JSONDecodeError
from pygame import display

from data.gui_texts import LANGUAGES


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
                "language" in data and
                "resolution" in data and
                data["language"] in LANGUAGES and
                data["resolution"] in SUPPORTED_RESOLUTIONS)

    def write_default_data():
        with open(_CONFIG_FILE, "w", encoding='utf-8') as f:
            data = {"language": LANGUAGES[0], "resolution": _max_available_resolution()}
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


def load_resolution():
    """Returns game resolution loaded from 'config.json'."""
    _validate_config()
    with open(_CONFIG_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data["resolution"]


def load_language():
    """Returns game language loaded from 'config.json'."""
    _validate_config()
    with open(_CONFIG_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return LANGUAGES.index(data["language"])


def save_resolution(text_resolution: str):
    """Saves new game resolution to 'config.json'."""
    _validate_config()
    with open(_CONFIG_FILE, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data["resolution"] = list(map(int, text_resolution.split(' x ')))
        file.seek(0)
        file.truncate(0)
        json.dump(data, file, ensure_ascii=False, indent=4)


def save_language(language: int):
    """Saves new game language to 'config.json'."""
    _validate_config()
    with open(_CONFIG_FILE, 'r+', encoding='utf-8') as file:
        data = json.load(file)
        data["language"] = language
        file.seek(0)
        file.truncate(0)
        json.dump(data, file, ensure_ascii=False, indent=4)


# Make sure that the directory for config file exists
user_dir = os.path.join(os.path.abspath(os.path.expanduser("~")), f".Underwater_Battles")
if not os.path.exists(user_dir):
    os.mkdir(user_dir)

_CONFIG_FILE = os.path.join(user_dir, 'config.json')


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


__all__ = [

    "SUPPORTED_RESOLUTIONS",
    "load_resolution",
    "load_language",
    "save_resolution",
    "save_language",

]
