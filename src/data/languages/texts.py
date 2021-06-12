import json
import os
import sys
from collections import defaultdict


def _init_texts() -> defaultdict(list):
    """Returns dictionary that stores all game text data in different languages. """
    texts = defaultdict(list)

    # paths to language files
    root_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    english_file_path = os.path.abspath(os.path.join(root_dir, "%s" % "english.json"))
    russian_file_path = os.path.abspath(os.path.join(root_dir, "%s" % "russian.json"))

    # Load text data from all language files and save it to TEXTS.
    for file_path in (english_file_path, russian_file_path):
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
