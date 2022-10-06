import logging
import sys
import time
from typing import List

import fastapi
from models import FlightsModel
from utils.file_reader import parse_response_file

api = fastapi.FastAPI()

FORMAT = '%(asctime)s : %(message)s'
logging.basicConfig(format=FORMAT, stream=sys.stdout, )
logger = logging.getLogger()
logger.setLevel('INFO')


@api.post('/search/', status_code=200, response_model=List[FlightsModel])
async def search_flight():
    flights = parse_response_file('./response_b.json')

    time.sleep(60)

    return flights
