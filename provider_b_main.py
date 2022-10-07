
import time
from typing import List

import fastapi
from models.flights import FlightsModel
from utils.file_reader import parse_response_file

api = fastapi.FastAPI()


@api.post('/search/', status_code=200, response_model=List[FlightsModel])
async def search_flight():
    flights = parse_response_file('./response_b.json')

    time.sleep(10)

    return flights
