import os
import json
from components.utils import HF


def _init_seekers_coords() -> dict:
    """Returns data about seekers coordinates, loaded from json files
    and converted to appropriate format.
    """

    def converted_data(json_data) -> dict:
        """Returns json data converted to appropriate format. """
        result = dict()
        for interval, coordinates in json_data.items():
            for pos in coordinates:
                pos[0] = HF(pos[0])
            min_health, max_health = map(int, interval.split())
            for health in range(min_health, max_health + 1):
                result[health] = coordinates
        return result

    seekers_coords = dict()
    root_dir = os.path.abspath(os.path.dirname(__file__))
    all_files = [f for f in os.listdir(root_dir) if f.endswith('.json')]

    for file in all_files:
        name = file.split('.')[0]
        file_path = os.path.join(root_dir, file)
        with open(file_path, 'r') as f:
            data = converted_data(json.load(f))
            seekers_coords[name] = data

    return seekers_coords


SEEKERS_COORDS = _init_seekers_coords()


__all__ = ["SEEKERS_COORDS"]
