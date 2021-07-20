import os
import json
from components.utils import HF


def _init_circle_offsets() -> list:
    root_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(root_dir, "circle_offsets.json")
    with open(file_path, 'r') as file:
        data = json.load(file)
        for coords in data:
            coords[0] = HF(coords[0])
        return data


CIRCLE_OFFSETS = _init_circle_offsets()


__all__ = ["CIRCLE_OFFSETS"]
