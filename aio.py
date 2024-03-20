#!/usr/bin/env python
# encoding: utf-8

import asyncio
import aiohttp

host = 'http://www.baidu.com'
urls_todo = {'/', '/1', '/2', '/3', '/4', '/5', '/6', '/7', '/8', '/9'}


async def fetch(session, url):
    async with session.get(url) as response:
        response = await response.read()
        return response


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, host + url) for url in urls_todo]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    import time
    start = time.time()
    asyncio.run(main())
    print(time.time() - start)
