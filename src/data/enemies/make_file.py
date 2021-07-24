import os
import json
from math import pi

from components.utils import *

print_circle_params(-151 - 219.0, -0, 146 - 62, 631)

circles_data = {
    "0 99": [
        {"type": "thick_blue", "radius": 135.404, "distance": 0, "angle": 0.0 * pi},
        {"type": "blue", "radius": 50.206, "distance": 143.372, "angle": 0.27 * pi},
        {"type": "blue", "radius": 50.206, "distance": 143.372, "angle": -0.27 * pi},
    ],
    "100 199": [
        {"type": "thick_blue", "radius": 135.404, "distance": 0, "angle": 0.0 * pi},
        {"type": "blue", "radius": 50.206, "distance": 143.372, "angle": 0.27 * pi},
        {"type": "blue", "radius": 50.206, "distance": 143.372, "angle": -0.27 * pi},
        {"type": "blue", "radius": 50.206, "distance": 130.46, "angle": 0.0 * pi},
    ],
    "200 299": [
        {"type": "thick_blue", "radius": 135.404, "distance": 0, "angle": 0.0 * pi},
        {"type": "blue", "radius": 50.206, "distance": 143.372, "angle": 0.27 * pi},
        {"type": "blue", "radius": 50.206, "distance": 143.372, "angle": -0.27 * pi},
        {"type": "blue", "radius": 50.206, "distance": 130.46, "angle": 0.0 * pi},
        {"type": "blue", "radius": 31.949, "distance": 140.729, "angle": 1.0 * pi},
    ],
    "300 400": [
        {"type": "thick_blue", "radius": 135.404, "distance": 0, "angle": 0.0 * pi},
        {"type": "blue", "radius": 50.206, "distance": 143.372, "angle": 0.27 * pi},
        {"type": "blue", "radius": 50.206, "distance": 143.372, "angle": -0.27 * pi},
        {"type": "blue", "radius": 50.206, "distance": 130.46, "angle": 0.0 * pi},
        {"type": "blue", "radius": 31.949, "distance": 143.561, "angle": 0.767 * pi},
        {"type": "blue", "radius": 31.949, "distance": 143.561, "angle": -0.767 * pi},
    ],
}

circles_list = dict_to_list(circles_data)

data = {
    "circles": circles_list,
    "circles states": make_states_dict(circles_data, circles_list),
    "guns": [
        {
            "name": "gun_18",
            "scale": 1.269,
            "distance": 0,
            "angle": 0,
            "rotation type": 1,
            "rotation angle": 0,
            "shooting type": "machine gun",
            "cooldown min": 100,
            "cooldown max": 100,
            "delay": 1800,
            "bullet name": "small red",
            "bullet velocity": 0.96,
            "bullet damage": -2
        },
        {
            "name": "seeker_spawner_2",
            "scale": 1.5,
            "distance": 168.671,
            "angle": 0.269 * pi,
            "rotation type": 0,
            "rotation angle": 0.269 * pi,
            "shooting type": "spawn orbital seeker",
            "cooldown min": 1800,
            "cooldown max": 1800,
            "delay": 2400,
            "bullet name": "enemy orbital seeker",
            "bullet velocity": 0.42,
            "bullet damage": -5
        },
        {
            "name": "seeker_spawner_2",
            "scale": 1.5,
            "distance": 168.671,
            "angle": -0.269 * pi,
            "rotation type": 0,
            "rotation angle": -0.269 * pi,
            "shooting type": "spawn orbital seeker",
            "cooldown min": 1800,
            "cooldown max": 1800,
            "delay": 2400,
            "bullet name": "enemy orbital seeker",
            "bullet velocity": 0.42,
            "bullet damage": -5
        },
    ],
    "guns states": {
        "0 400": [0, 1, 2],
    },
    "radius": 125.404,
    "rect size": 400.105,
    "max health": 400,
    "velocity": 0.0,
    "death award": {
        "medium": 10,
        "large": 5,
        "ultra": 3
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


#_make_enemy("BossRightHand")
