import os
import json
from math import pi

from components.utils import *

print_circle_params(-578, -573, 336, 1995)

circles_data = {
    "0 39": [
        {"type": "blue", "radius": 24.06, "distance": 50.369, "angle": 0.256 * pi},
        {"type": "blue", "radius": 24.06, "distance": 50.369, "angle": -0.256 * pi},
        {"type": "blue", "radius": 24.06, "distance": 51.125, "angle": 0.748 * pi},
        {"type": "blue", "radius": 24.06, "distance": 51.125, "angle": -0.748 * pi},

        {"type": "thick_blue", "radius": 39.218, "distance": 1.444, "angle": 1.0 * pi},
    ],
    "40 60": [
        {"type": "blue", "radius": 11.008, "distance": 44.439, "angle": 0.296 * pi},
        {"type": "blue", "radius": 11.008, "distance": 44.439, "angle": -0.296 * pi},
        {"type": "blue", "radius": 11.008, "distance": 43.475, "angle": 0.187 * pi},
        {"type": "blue", "radius": 11.008, "distance": 43.475, "angle": -0.187 * pi},
        {"type": "blue", "radius": 24.06, "distance": 72.216, "angle": 0.235 * pi},
        {"type": "blue", "radius": 24.06, "distance": 72.216, "angle": -0.235 * pi},

        {"type": "blue", "radius": 11.008, "distance": 45.311, "angle": 0.811 * pi},
        {"type": "blue", "radius": 11.008, "distance": 45.311, "angle": -0.811 * pi},
        {"type": "blue", "radius": 11.008, "distance": 45.55, "angle": 0.709 * pi},
        {"type": "blue", "radius": 11.008, "distance": 45.55, "angle": -0.709 * pi},
        {"type": "blue", "radius": 24.06, "distance": 73.69, "angle": 0.758 * pi},
        {"type": "blue", "radius": 24.06, "distance": 73.69, "angle": -0.758 * pi},

        {"type": "thick_blue", "radius": 39.218, "distance": 1.444, "angle": 1.0 * pi},
    ],
}

circles_list = dict_to_list(circles_data)

data = {
    "circles": circles_list,
    "circles states": make_states_dict(circles_data, circles_list),
    "guns": [
        {
            "name": "turret",
            "scale": 1,
            "distance": 1.444,
            "angle": pi,
            "rotation type": 2,
            "rotation angle": 0,
            "shooting type": "machine gun 360",
            "cooldown min": 40,
            "cooldown max": 40,
            "delay": 2000,
            "bullet name": "small red",
            "bullet velocity": 1.08,
            "bullet damage": -2
        }
    ],
    "guns states": {
        "0 60": [0],
    },
    "radius": 46.421,
    "rect size": 97.911 * 2,
    "max health": 60,
    "velocity": 0.0,
    "death award": {
        "medium": 30,
        "large": 0,
        "ultra": 0
    },
    "spawners": [
    ],
    "events": [
    ]
}


def _make_enemy(name):
    file_name = name + '.json'
    root_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(root_dir, file_name)
    with open(path, 'w') as file:
        json.dump(data, file)


#_make_enemy("SmallTurret")
