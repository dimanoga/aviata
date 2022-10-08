import json
import uuid
from urllib.error import HTTPError

import aiohttp

from database.utils import update_search_result, get_search_result
from logger import logger
from schemas.flights import FlightsModel


async def get_flights(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(url) as response:
            try:
                response = await response.json(encoding='UTF-8')
            except HTTPError:
                logger.debug(f'Something went wrong for url {url}')
            return [FlightsModel.parse_obj(item) for item in response]


async def process_result(search_id: uuid.UUID, url: str) -> None:
    logger.info(f'Start request to url - {url}')
    data = await get_flights(url=url)
    data = [data.dict() for data in data]
    search_result = get_search_result(search_id=search_id)
    if search_result.status == "COMPLETED":
        data = search_result.data + data
    update_search_result(search_id=search_id, data=data)
