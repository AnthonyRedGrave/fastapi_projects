from datetime import timedelta
from fastapi import FastAPI
import httpx
from scrapy.selector import Selector
# from fastapi_redis import redis_client
import redis

app = FastAPI()


@app.get('/api/weather/{city}')
async def weather(city: str):
    # redis = await aioredis.create_redis(address=('redis', 6379))
    r = redis.Redis(host='redis', port=6379, db=0)

    #get cache from memory
    cache = r.get(city)
    #check value from cache, if exists return it
    if cache is not None:
        print("CACHE")
        return {'city': city, 'temp': cache}
    

    url = f'https://pogoda.mail.ru/prognoz/{city}/'

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()

    selector = Selector(text = response.text)
    # t = selector.xpath('//div[@class="information__content__temperature"]/text()').getall()[1].strip()
    t = selector.xpath('//div[@class="information__content__temperature"]/text()').getall()[1].strip()
    r.set(city, t)
    return {'city': city, 'temp': t}
