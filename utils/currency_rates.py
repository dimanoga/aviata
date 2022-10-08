import datetime

from typing import Dict

import aiohttp
import aioredis
import xmltodict

from logger import logger
from utils.expire_timestamp import get_expire_timestamp


async def get_rates(redis: aioredis.Redis, currency: str) -> float:
    cache = await redis.get(currency)
    if cache is not None:
        return float(cache)
    rates = await cache_currency(redis=redis)
    return rates.get(currency)


async def cache_currency(redis: aioredis.Redis) -> Dict:
    logger.info('Start cashing currencies')
    now_date = datetime.date.today().strftime('%d.%m.%Y')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.nationalbank.kz/rss/get_rates.cfm?fdate={now_date}') as response:
            response = await response.text(encoding='UTF-8')
            response = xmltodict.parse(response)
    rates = {rate['title']: rate['description'] for rate in response['rates']['item']}
    for currency, price in rates.items():
        await redis.set(currency, float(price))
        await redis.expireat(currency, get_expire_timestamp())
    return rates
