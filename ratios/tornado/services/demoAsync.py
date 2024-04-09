#!/usr/bin/env python3

import asyncio
import time
from datetime import timedelta


from tornado import gen, httpclient, queues

from rava import urls as urls_base

concurrency = 10


async def fetchFromUrl(url):

    response = await httpclient.AsyncHTTPClient().fetch(url)

    return  response

def getUrl(ticker):
    return  urls_base['perfilRava']+'/'+ticker

async def main():
    q = queues.Queue()
    fetching, fetched, dead = set(), set(), set()

    tickers = ['pep','pg', 'al30', 'al30d']
    [q.put(ticker) for ticker in tickers]

    async def fetchTicker(currentTicker):
        if currentTicker in fetching:
            return

        print("fetching %s" % currentTicker)
        fetching.add(currentTicker)
        url = getUrl(currentTicker)
        # response = await fetchFromUrl(url)
        fetched.add(currentTicker)

    async def worker():
        async for ticker in q:
            if ticker is None:
                return
            try:
                await fetchTicker(ticker)
            except Exception as e:
                dead.add(ticker)
            finally:
                q.task_done()

    # Start workers, then wait for the work queue to be empty.

    start = time.time()
    workers = gen.multi([worker() for _ in range(concurrency)])
    await q.join(timeout=timedelta(seconds=300))
    assert fetching == (fetched | dead)
    print("Done in %d seconds, fetched %s URLs." % (time.time() - start, len(fetched)))
    print("Unable to fetch ",  dead)
    print("Fetched ", fetched)

    # Signal all the workers to exit.
    for _ in range(concurrency):
        await q.put(None)
    await workers


if __name__ == "__main__":

    asyncio.run(main())