import asyncio
from demoAsync import asyncFetcher
from rava import getCuadroTecnico

async def main():

    tickers = ['pep','pg', 'al30', 'al30d']
    urls = [f"https://www.rava.com/perfil/{ticker}"  for ticker in tickers]
    responses = await asyncFetcher(urls)

    for response in responses:
        print(getCuadroTecnico(response['response']))


if __name__ == "__main__":

    asyncio.run(main())