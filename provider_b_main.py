
import time
from typing import List

import fastapi
from schemas.flights import FlightsModel
from utils.file_reader import parse_response_file

api = fastapi.FastAPI()


@api.post('/search/', status_code=200)
async def search_flight():
    flights = parse_response_file('./response_b.json')

    time.sleep(10)

    return flights
