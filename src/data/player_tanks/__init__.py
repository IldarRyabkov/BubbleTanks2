import os
import json
from components.utils import HF


def _converted_data(json_data) -> dict:
    """Returns json data converted to appropriate format. """

    def convert_keys(d: dict) -> dict:
        """Converts dictionary keys from string to tuple format.
        {'1 2': 3} -> {(1, 2): 3}
        """
        return {tuple(map(int, k.split())): v for k, v in d.items()}

    json_data["circles states"] = convert_keys(json_data["circles states"])
    json_data["guns states"] = convert_keys(json_data["guns states"])

    for key in ("radius", "background radius", "max velocity"):
        json_data[key] = HF(json_data[key])

    return json_data


def _init_player_tanks() -> dict:
    """Initialises dictionary that stores all
    data about player tanks loaded from json files.
    """
    root_dir = os.path.abspath(os.path.dirname(__file__))
    tanks_data = {}
    all_files = [f for f in os.listdir(root_dir) if f.endswith('.json')]
    for file_name in all_files:
        file_path = os.path.join(root_dir, file_name)
        if file_name.startswith('empty'):
            tank = 'empty'
        else:
            tank = (int(file_name[0]), int(file_name[1]))
        with open(file_path, 'r') as f:
            data = _converted_data(json.load(f))
            tanks_data[tank] = data
    return tanks_data


PLAYER_TANKS = _init_player_tanks()


__all__ = ["PLAYER_TANKS"]
