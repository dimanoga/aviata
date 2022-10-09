import uuid

import aioredis as aioredis

from fastapi import BackgroundTasks, FastAPI
from pydantic.error_wrappers import ValidationError

from custom_exceptions import SEARCH_NOT_FOUND, CURRENCY_NOT_FOUND, CurrencyNotFound
from database.requests_model import StatusEnum
from database.utils import create_search_request, get_search_request, create_search_result, create_db
from schemas.airflow import ResponseModel, SearchResultModel, PriceModel
from schemas.requests import RequestSchema
from settings import RequestSettings, DBSettings
from utils.currency_rates import get_rates, cache_currency
from utils.search_flights import process_result

api = FastAPI()

@api.post('/search/', status_code=200, response_model=ResponseModel)
async def search_flight(background_tasks: BackgroundTasks):
    request_settings = RequestSettings()
    search_id = uuid.uuid4()
    background_tasks.add_task(process_result, search_id=search_id, url=request_settings.provider_a_url + '/search')
    background_tasks.add_task(process_result, search_id=search_id, url=request_settings.provider_b_url + '/search')
    await create_search_request(search_id=search_id, status=StatusEnum.pending)
    return {'search_id': search_id}


@api.post('/results/{search_id}/{currency}', status_code=200, response_model=SearchResultModel)
async def get_flight(search_id: uuid.UUID, currency: str, background_tasks: BackgroundTasks):
    """ Получаем резульаты поиска по уникальному search_id и конвертируем сумму в валюту currency"""
    redis = await aioredis.create_redis(address=('redis', 6379))
    currency = currency.upper()

    try:
        search_request = await get_search_request(search_id=search_id)
    except ValidationError:
        raise SEARCH_NOT_FOUND
    search_request = RequestSchema.from_orm(search_request)
    if search_request.status == 'PENDING':
        return {'search_id': search_id,
                'status': search_request.status,
                'data': []}

    try:
        currency_price = await get_rates(redis, currency)
    except CurrencyNotFound:
        raise CURRENCY_NOT_FOUND

    search_request = SearchResultModel(search_id=search_request.search_id,
                                       status=search_request.status,
                                       data=[item for item in search_request.data])
    response = []
    for item in search_request.data:
        item.price = PriceModel(amount=0, currency=currency)
        if item.pricing.currency == currency:
            item.price.amount = item.pricing.total
            response.append(item)
        else:
            if item.pricing.currency == 'KZT':
                kzt_amount = item.pricing.total
            else:
                try:
                    currency_from = await get_rates(redis, item.pricing.currency)
                except CurrencyNotFound:
                    raise CURRENCY_NOT_FOUND
                kzt_amount = currency_from * item.pricing.total  # Переводим начальную валюту в тенге
            item.price.amount = round(kzt_amount / currency_price, 2)  # переводим тенге в конечную валюту
            item.price.currency = currency
            response.append(item)
    search_request.data = sorted(response, key=lambda i: i.price.amount, reverse=True)
    background_tasks.add_task(create_search_result, search_id=search_id, data=[data.dict() for data in response])
    return search_request


@api.on_event("startup")
async def startup():
    redis = await aioredis.create_redis(address=('redis', 6379))
    await cache_currency(redis=redis)
    
    create_db()
    
