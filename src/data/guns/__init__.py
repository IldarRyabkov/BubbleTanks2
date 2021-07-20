import os
import json


def _init_guns() -> dict:
    """Initialises dictionary that stores all
    data about guns loaded from json files.
    """
    root_dir = os.path.abspath(os.path.dirname(__file__))
    gun_bodies = {}
    all_files = [f for f in os.listdir(root_dir) if f.endswith('.json')]
    for file_name in all_files:
        gun_type = file_name.split('.')[0]
        file_path = os.path.join(root_dir, file_name)
        with open(file_path, 'r') as f:
            data = json.load(f)
            gun_bodies[gun_type] = data
    return gun_bodies


GUNS = _init_guns()


__all__ = ["GUNS"]
