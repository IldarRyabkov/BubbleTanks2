import os
import json


def _delete_element(element, data, result):
    for v in data:
        if element in v:
            index = v.index(element)
            if index != 0:
                elements = [v[i] for i in range(index)]
                for element in elements:
                    _delete_element(element, data, result)
    for v in data:
        if element in v:
            v.remove(element)
    if element not in result:
        result.append(element)


def _all_circles(circles_dict):
    data = list(v[:] for v in circles_dict.values())
    result = []
    while any(v for v in data):
        for v in data:
            if v:
                _delete_element(v[0], data, result)
                break
    return result


def _delete_wrong_circles(file_name):
    def wrong_circle(circle):
        return circle["type"] == "orange" and (abs(circle["angle"]) >= 0.5 * 3.141592653589793 or circle["distance"] <= 41.52)

    root_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(root_dir, file_name)
    with open(file_path, 'r') as f:
        data = json.load(f)
        circles = data["circles"]
        circles_dict = {k: [circles[i] for i in v if not wrong_circle(circles[i])] for k, v in data["circles states"].items()}
        all_circles = _all_circles(circles_dict)
        for k, v in circles_dict.items():
            circles_dict[k] = [all_circles.index(circle) for circle in v]
        data["circles"] = all_circles
        data["circles states"] = circles_dict
    with open(file_path, 'w') as f:
        json.dump(data, f)