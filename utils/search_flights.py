import uuid
from typing import List
from urllib.error import HTTPError

import aiohttp

from database.utils import update_search_request, get_search_request
from logger import logger
from schemas.flights import FlightsModel
from schemas.requests import RequestSchema


async def get_flights(url: str):
	""" Получаем список рейсов """
	async with aiohttp.ClientSession() as session:
		async with session.post(url) as response:
			try:
				response = await response.json(encoding='UTF-8')
			except HTTPError:
				logger.debug(f'Something went wrong for url {url}')
			return [FlightsModel.parse_obj(item) for item in response]


async def process_result(search_id: uuid.UUID, urls: List[str]) -> None:
	""" Записываем результаты поиска в базу """
	for url in urls:
		logger.info(f'Start request to url - {url}')
		data = await get_flights(url=url)
		data = [data.dict() for data in data]
		search_request = await get_search_request(search_id=search_id)
		if search_request:
			search_request = RequestSchema.from_orm(search_request)
			if search_request.status == "COMPLETED":
				data = search_request.data + data
		await update_search_request(search_id=search_id, data=data)
