import json
from json.decoder import JSONDecodeError
from pygame import display
from pathlib import Path
from data.paths import RESOLUTIONS


ALL_RESOLUTIONS = [
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


def max_res():
    return list(display.list_modes()[0])


def save_resolution(res):
    with open(RESOLUTIONS, 'w', encoding='utf-8') as file:
        json.dump(res, file, ensure_ascii=False, indent=4)


def get_resolution() -> list:
    """Returns screen resolution loaded from the file resolution.json.
    If file data is incorrect, returns maximum available
    resolution and saves it in file resolution.json.
    """
    if not Path(RESOLUTIONS).is_file():
        with open(RESOLUTIONS, "w") as write_file:
            json.dump('', write_file)

    with open(RESOLUTIONS, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except JSONDecodeError:
            res = None
        else:
            if type(data) == list and len(data) == 2 and all(type(x) == int for x in data):
                res = data
            else:
                res = None

    display.init()
    if res is None or not (res == max_res() or res in ALL_RESOLUTIONS):
        res = max_res()
        save_resolution(res)

    return res


def cur_res_index():
    available = [res for res in ALL_RESOLUTIONS if res <= max_res()]
    if available[-1] != max_res():
        available.append(max_res())
    return available.index(get_resolution())


def get_available_resolutions():
    available = [res for res in ALL_RESOLUTIONS if res <= max_res()]
    if available[-1] != max_res():
        available.append(max_res())
    return [pretty_resolution(res) for res in available]


def pretty_resolution(res):
    return '%d x %d' % tuple(res)


def raw_resolution(res):
    return list(map(int, res.split(' x ')))


__all__ = [

    "save_resolution",
    "get_resolution",
    "get_available_resolutions",
    "raw_resolution",
    "cur_res_index",
    "ALL_RESOLUTIONS"

]