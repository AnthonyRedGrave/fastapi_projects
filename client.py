import asyncio
import httpx
import time
import grequests

async def get_api_data(city):
    url = f'http://0.0.0.0:8080/api/weather/{city}'

    requests = [
        grequests.get(url),
        grequests.get(url),
        grequests.get(url),
        grequests.get(url),
        grequests.get(url),
        grequests.get(url)
    ]
    for resp in grequests.imap(requests, size=6):
        # print(resp)
        print(resp.json())

tasks = [
    asyncio.ensure_future(get_api_data('moskva')),
    asyncio.ensure_future(get_api_data('minsk')),
    asyncio.ensure_future(get_api_data('london'))
]

start = time.time()

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(*tasks))
loop.close()

end_time = time.time() - start

print(f"time {end_time:0.2f} seconds")