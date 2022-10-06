import logging
import sys

import fastapi
import httpx
import aioredis

api = fastapi.FastAPI()

FORMAT = '%(asctime)s : %(message)s'
logging.basicConfig(format=FORMAT, stream=sys.stdout, )
logger = logging.getLogger()
logger.setLevel('INFO')


@api.post('/api/weather/{city}')
async def weather(city: str):
    redis = await aioredis.create_redis(address=('redis', 6379))

    # get cache from memory
    cache = await redis.get(city)

    # check value from cache, if exists return it
    if cache is not None:
        return {'city': city, 'temperature': cache, 'source': 'cache'}

    url = f'https://pogoda.mail.ru/prognoz/{city}/'

    # asynchronous implementation
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

    selector = Selector(text=response.text)
    t = selector.xpath('//div[@class="information__content__temperature"]/text()').getall()[1].strip()

    # save cache in memory for 1 hour
    await redis.set(city, t, expire=3600)

    return {'city': city, 'temperature': t, 'source': 'pogoda.mail.ru'}
