import os
import json
from math import pi

from components.utils import print_circle_params


circles = [
        {"type": "orange", "radius": 10.414, "distance": 17.197, "angle": 0.0 * pi},
        {"type": "orange", "radius": 10.414, "distance": 0, "angle": 0.0 * pi},
        {"type": "orange", "radius": 10.414, "distance": 48.972, "angle": 0.143 * pi},
        {"type": "orange", "radius": 10.414, "distance": 48.972, "angle": -0.143 * pi},
        {"type": "orange", "radius": 16.863, "distance": 38.455, "angle": 0.0 * pi},
        {"type": "orange", "radius": 14.188, "distance": 67.085, "angle": 0.151 * pi},
        {"type": "orange", "radius": 14.188, "distance": 67.085, "angle": -0.151 * pi},
        {"type": "orange", "radius": 10.414, "distance": 64.792, "angle": 0.246 * pi},
        {"type": "orange", "radius": 10.414, "distance": 64.792, "angle": -0.246 * pi},
        {"type": "orange", "radius": 15.478, "distance": 66.742, "angle": 0.336 * pi},
        {"type": "orange", "radius": 15.478, "distance": 66.742, "angle": -0.336 * pi},
        {"type": "swinging", "color": "light orange", "radius": 16.863, "distance": 40.148, "angle": 0.222 * pi, "swing distance": 51.592, "swing angle": -0.5 * pi},
]

print_circle_params(792-168, -270*2, 472, 1000)

data = {
    "circles": circles,
    "size": 16.863,
    "emitter offset": 78.842,
    "bullet type": "enemy leecher"
}


def _make_file(name):
    root_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(root_dir, name)
    with open(path, 'w') as file:
        json.dump(data, file)


#_make_file("leecher_spawner.json")
