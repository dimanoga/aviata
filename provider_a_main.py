import asyncio

import fastapi
from utils.file_reader import parse_response_file

api = fastapi.FastAPI()


@api.post('/search/', status_code=200)
async def search_flight():
    flights = parse_response_file('./response_a.json')

    await asyncio.sleep(30)

    return flights
