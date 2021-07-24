import os
import json


def _init_shapes() -> dict:
    """Initialises dictionary that stores all
    data about shapes loaded from json files.
    """
    root_dir = os.path.abspath(os.path.dirname(__file__))
    shapes = {}
    all_files = [f for f in os.listdir(root_dir) if f.endswith('.json')]
    for file_name in all_files:
        file_path = os.path.join(root_dir, file_name)
        shape_name = file_name.split('.')[0]
        with open(file_path, 'r') as f:
            shapes[shape_name] = json.load(f)
    return shapes


SHAPES = _init_shapes()


__all__ = ["SHAPES"]
