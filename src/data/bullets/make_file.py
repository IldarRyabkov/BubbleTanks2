import os
import json

from components.utils import print_circle_params
from math import pi


print_circle_params(317*2, -208*2, 878, 3981)


def _make_file(name):
    data = {
        "radius": 18.87,
        "circles":  [
            {"type":  "scaling", "color": "red", "radius": 18.87, "edge factor": 0.122, "amplitude factor": 0.347, "distance":  3.738, "angle": 0.0 * pi},
            {"type":  "fixed", "color": "red", "radius": 7.536, "edge factor": 0.122, "distance":  19.028, "angle": 0.799 * pi},
            {"type":  "fixed", "color": "red", "radius": 7.536, "edge factor": 0.122, "distance":  19.028, "angle": -0.799 * pi},
            {"type":  "swinging", "color": "red", "radius": 5.607, "edge factor": 0.218, "distance":  31.47, "angle": 0.876 * pi, "swing distance": 8.615, "swing angle": 0.25 * pi},
            {"type":  "swinging", "color": "red", "radius": 5.607, "edge factor": 0.218, "distance":  31.47, "angle": -0.876 * pi, "swing distance": 8.615, "swing angle": -0.25 * pi},
        ],
        "hit effect": "RedCircle"
    }
    root_dir = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(root_dir, "%s.json" % name)
    with open(path, 'w') as file:
        json.dump(data, file)


#_make_file("enemy_sapper")