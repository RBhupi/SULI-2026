import json
import os


def safe_json_load(path, default=None):

    if not os.path.exists(path):
        return default or {}

    with open(path, "r") as f:
        return json.load(f)


def safe_json_write(path, data):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def chunk_list(data, size):

    for i in range(0, len(data), size):
        yield data[i:i + size]


def to_float(value):

    try:
        return float(value)
    except:
        return None


def normalize_column(name: str) -> str:
    return name.strip().lower()