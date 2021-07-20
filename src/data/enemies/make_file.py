import os
import json
from math import pi

from components.utils import *


print_circle_params(-11, 301, (78 + 99) / 2, 1259)

circles_data = {
    "0 50": [
        {"type": "confusion", "radius": 113.28, "distance": 0, "angle": 0.0 * pi},
    ],
}

circles_list = dict_to_list(circles_data)

data = {
    "circles": circles_list,
    "circles states": make_states_dict(circles_data, circles_list),
    "guns": [

    ],
    "guns states": {
        "0 50": [],
    },
    "radius": 107.28,
    "rect size": 113.28*2,
    "max health": 50,
    "velocity": 0.06,
    "death award": {
        "medium": 7,
        "large": 4,
        "ultra": 0
    },
    "spawners": [
    ],
    "events": [
        {
            "trigger value": -1,
            "action": "change color",
            "value": None
        }
    ]
}


def _make_enemy(name):
    file_name = name + '.json'
    root_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(root_dir, file_name)
    with open(path, 'w') as file:
        json.dump(data, file)


#_make_enemy("Confusasdion")
