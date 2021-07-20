import os
import json


def _init_bubbles() -> dict:
    bubbles = {}
    root_dir = os.path.abspath(os.path.dirname(__file__))
    all_files = [f for f in os.listdir(root_dir) if f.endswith('.json')]

    for file in all_files:
        name = file.split('.')[0]
        file_path = os.path.join(root_dir, file)
        with open(file_path, 'r') as f:
            bubbles[name] = json.load(f)
    return bubbles


BUBBLES = _init_bubbles()


__all__ = ["BUBBLES"]
