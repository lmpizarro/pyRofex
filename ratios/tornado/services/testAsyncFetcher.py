import asyncio
from asyncHttpDowload import asyncFetcher

async def main():

    tickers = ['pep','pg', 'al30', 'al30d']
    urls = [f"https://www.rava.com/perfil/{ticker}"  for ticker in tickers]
    responses = await asyncFetcher(urls)

    for response in responses:
        print(response)


if __name__ == "__main__":

    asyncio.run(main())