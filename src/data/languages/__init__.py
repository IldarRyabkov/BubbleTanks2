import json
import os
from os import listdir
from collections import defaultdict


def _init_texts():
    """Returns dictionary that stores all game text data in different languages. """
    texts = defaultdict(list)

    root_dir = os.path.abspath(os.path.dirname(__file__))
    json_files = [f for f in listdir(root_dir) if f.endswith('.json')]

    for file_name in json_files:
        file_path = os.path.join(root_dir, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for key, value in data.items():
                texts[key].append(value)

    # Manually change keys of tank descriptions from strings like "0 0" to tuples like (0, 0),
    # because json doesn't support these keys.
    for i, language in enumerate(texts["tank descriptions"]):
        texts["tank descriptions"][i] = {tuple(map(int, k.split())): v for k, v in language.items()}

    # Manually create data about tank names, based on tank descriptions
    for language in texts["tank descriptions"]:
        tank_names = {k: v[0] for k, v in language.items()}
        texts["tank names"].append(tank_names)

    return texts


TEXTS = _init_texts()


__all__ = ["TEXTS"]
