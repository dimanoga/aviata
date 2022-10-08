import asyncio
import uuid

import aioredis as aioredis
from fastapi import BackgroundTasks, FastAPI

from database.requests_model import StatusEnum
from database.utils import create_search_result
from schemas.airflow import ResponseModel
from settings import RequestSettings
from utils.currency_rates import get_rates, cache_currency
from utils.search_flights import get_flights, process_result

api = FastAPI()


@api.post('/search/', status_code=200, response_model=ResponseModel)
async def search_flight(background_tasks: BackgroundTasks):
    request_settings = RequestSettings()
    search_id = uuid.uuid4()
    background_tasks.add_task(process_result, search_id=search_id, url=request_settings.provider_a_url + '/search')
    background_tasks.add_task(process_result, search_id=search_id, url=request_settings.provider_b_url + '/search')
    create_search_result(search_id=search_id, status=StatusEnum.pending)
    return {'search_id': search_id}


async def get_flight():
    redis = await aioredis.create_redis(address=('127.0.0.1', 6379))
    print(await get_rates(redis, 'RUB'))


@api.on_event("startup")
async def cache_currencies():
    redis = await aioredis.create_redis(address=('127.0.0.1', 6379))
    await cache_currency(redis=redis)
