import json
import os


def get_file_path(filename):
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, "data", filename)


def read_data(filename):
    file_path = get_file_path(filename)

    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

    return data


def write_data(filename, data):
    file_path = get_file_path(filename)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)