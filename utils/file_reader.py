import json

from typing import List

from models.flights import FlightsModel


def parse_response_file(file_path: str) -> List[FlightsModel]:
    with open(file_path) as json_data:
        data = json.load(json_data)

    return [FlightsModel.parse_obj(item) for item in data]
