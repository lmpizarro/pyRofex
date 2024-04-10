#!/usr/bin/env python3

import asyncio
import time
from datetime import timedelta
from tornado import gen, httpclient, queues

from rava import urls as urls_base, getCuadroTecnico

concurrency = 10


def getUrlRavaPerfil(ticker):
    return  urls_base['perfilRava']+'/'+ticker

async def asyncFetcher(urls):

    queue = queues.Queue()
    fetching, fetched, dead = set(), set(), set()
    responses = []

    [queue.put(url) for url in urls]

    async def fetchUrl(url):
        if url in fetching:
            return

        print("fetching %s" % url)
        fetching.add(url)
        response = await httpclient.AsyncHTTPClient().fetch(url)
        responses.append({'url': url, 'response': response})
        fetched.add(url)

    async def worker():
        async for url in queue:
            if url is None:
                return
            try:
                await fetchUrl(url)
            except Exception as e:
                dead.add(url)
            finally:
                queue.task_done()

    # Start workers, then wait for the work queue to be empty.

    start = time.time()
    workers = gen.multi([worker() for _ in range(concurrency)])
    await queue.join(timeout=timedelta(seconds=300))
    assert fetching == (fetched | dead)
    print("Done in %d seconds, fetched %s URLs." % (time.time() - start, len(fetched)))
    print("Unable to fetch ",  dead)
    print("Fetched ", fetched)

    # Signal all the workers to exit.
    for _ in range(concurrency):
        await queue.put(None)
    await workers

    return responses

async def main():

    tickers = ['pep','pg', 'al30', 'al30d']
    urls = [getUrlRavaPerfil(ticker) for ticker in tickers]
    responses = await asyncFetcher(urls)

    for response in responses:
        print(response['url'].split('/')[-1], getCuadroTecnico(response['response']))


if __name__ == "__main__":

    asyncio.run(main())