import os
import json

from components.utils import HF, H


def _converted_data(json_data) -> dict:
    """Returns json data converted to appropriate format. """

    def convert_keys(d: dict) -> dict:
        """Converts dictionary keys from string to tuple format.
        {'1 2': 3} -> {(1, 2): 3}
        """
        return {tuple(map(int, k.split())): v for k, v in d.items()}

    json_data["circles states"] = convert_keys(json_data["circles states"])
    json_data["guns states"] = convert_keys(json_data["guns states"])
    json_data["radius"] = HF(json_data["radius"])
    json_data["velocity"] = HF(json_data["velocity"])
    json_data["rect size"] = H(json_data["rect size"])
    for spawner in json_data["spawners"]:
        spawner["distance"] = HF(spawner["distance"])

    return json_data


def _init_enemies() -> dict:
    """Initialises dictionary that stores all
    data about enemies loaded from json files.
    """
    root_dir = os.path.abspath(os.path.dirname(__file__))
    enemies = {}
    all_files = [f for f in os.listdir(root_dir) if f.endswith('.json')]
    for file_name in all_files:
        file_path = os.path.join(root_dir, file_name)
        enemy_name = file_name.split('.')[0]
        with open(file_path, 'r') as f:
            enemy_data = _converted_data(json.load(f))
            enemies[enemy_name] = enemy_data
    return enemies


ENEMIES = _init_enemies()


__all__ = ["ENEMIES"]
