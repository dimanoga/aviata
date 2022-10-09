import json

from pydantic.types import Json


def parse_response_file(file_path: str) -> Json:
    with open(file_path) as json_data:
        data = json.load(json_data)

    return data
