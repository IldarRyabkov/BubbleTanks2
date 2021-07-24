import os
import json
from math import pi

from components.utils import print_circle_params


print_circle_params(-0, -1817-(2137-1817) + 1544.0, 2137-1817, 631)


data = {
    "circles": [
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 74.168, "distance": 288.685, "angle": -0.5 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 84.437, "distance": 192.456, "angle": -0.5 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 94.326, "distance": 76.45, "angle": -0.5 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 78.732, "distance": 62.007, "angle": 0.994 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 78.732, "distance": 62.007, "angle": 0.006 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 87.861, "distance": 97.75, "angle": 0.5 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 67.512, "distance": 162.176, "angle": 0.751 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 67.512, "distance": 162.176, "angle": 0.249 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 121.712, "distance": 225.547 , "angle": 0.5 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 92.044, "distance": 285.53, "angle": 0.68 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 92.044, "distance": 285.53, "angle": 0.32 * pi, "glares angle": 0.0 * pi},
        {"type": "static", "color": "purple", "edge factor": 0.046, "radius": 139.208, "distance": 356.006, "angle": 0.5 * pi, "glares angle": 0.0 * pi},

    ],
    "distance": 587.258,
    "angle": 0.5 * pi,
    "width": 486.086,
    "height": 722.466,
}


def _make_file(name):
    file_name = name + '.json'
    root_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(root_dir, file_name)
    with open(path, 'w') as file:
        json.dump(data, file)


#_make_file("skasdeletoasdn_3")
