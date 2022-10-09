import datetime

from typing import Dict

import aiohttp
import aioredis
import xmltodict

from custom_exceptions import  CurrencyNotFound
from logger import logger
from utils.expire_timestamp import get_expire_timestamp


async def get_rates(redis: aioredis.Redis, currency: str) -> float:
    """ Получаем курс для заданной валюты currency """
    cache = await redis.get(currency)
    if cache is not None:
        return float(cache)
    rates = await cache_currency(redis=redis)

    currency_rate = rates.get(currency)
    if currency_rate is None:
        raise CurrencyNotFound(message=f'Currency {currency} not found')
    return float(currency_rate)


async def cache_currency(redis: aioredis.Redis) -> Dict:
    """ Получаем общий курс валют и эшируем в редис """
    logger.info('Start caching currencies')
    now_date = datetime.date.today().strftime('%d.%m.%Y')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.nationalbank.kz/rss/get_rates.cfm?fdate={now_date}') as response:
            response = await response.text(encoding='UTF-8')
            response = xmltodict.parse(response)
    rates = {rate['title']: rate['description'] for rate in response['rates']['item']}
    for currency, price in rates.items():
        await redis.set(currency, float(price))
        await redis.expireat(currency, get_expire_timestamp())
    logger.info('Done caching currencies')
    return rates
