import os
import json
from math import pi

from components.utils import print_circle_params


print_circle_params(438, -329, 380, 631)


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


data = [
    {"type": "fixed", "color": "violet", "edge factor": 0.05, "radius": 21.328, "distance": 29.437, "angle": 0.799 * pi},
    {"type": "fixed", "color": "violet", "edge factor": 0.05, "radius": 9.943, "distance": 28.294, "angle": 0.521 * pi},
    {"type": "fixed", "color": "violet", "edge factor": 0.05, "radius": 9.943, "distance": 34.919, "angle": 0.995 * pi},
    {"type": "fixed", "color": "violet", "edge factor": 0.05, "radius": 9.943, "distance": 22.448, "angle": -0.914 * pi},
    {"type": "fixed", "color": "violet", "edge factor": 0.05, "radius": 9.943, "distance": 36.833, "angle": -0.469 * pi},
    {"type": "fixed", "color": "violet", "edge factor": 0.05, "radius": 12.903, "distance": 42.885, "angle": 0.254 * pi},
]


def _make_shape(name):
    file_name = name + '.json'
    root_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(root_dir, file_name)
    with open(path, 'w') as file:
        json.dump(data, file)


SHAPES = _init_shapes()

#_make_shape("spawner")


__all__ = ["SHAPES"]
