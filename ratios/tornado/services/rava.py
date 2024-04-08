import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import tornado

urls = {
    "perfilRava": "https://www.rava.com/perfil",
    "dolar" : 'https://www.rava.com/cotizaciones/dolares'
}

class Asset:
    def __init__(self, ticker=None, price=None) -> None:
        self.ticker = ticker
        self.price = price

class AsyncFetcher:

    @staticmethod
    async def fetch(url: str):
        http_client = tornado.httpclient.AsyncHTTPClient()
        response = await http_client.fetch(url)
        return response


async def precioEspecie(ticker='ba37d'):
    ''' last price & properties '''
    url = f'https://www.rava.com/perfil/{ticker}'

    response = await AsyncFetcher.fetch(url)
    soup = BeautifulSoup(response.body, 'html.parser')

    table = soup.find("main").find("perfil-p")
    last = np.nan
    try:
        especie = json.loads(table.attrs[':res'])['cuad_tecnico'][0]
        varmensual = especie['varmensual']
        varanual = especie['varanual']
        last = float(especie['ultimonum'])
    except:
        pass

    return last

async def precioMep():
    url = urls['dolar']
    response = await AsyncFetcher.fetch(url)
    soup = BeautifulSoup(response.body, 'html.parser')
    table = soup.find(name='dolares-p')
    body = json.loads(table.attrs[":datos"])["body"]

    dolares = []
    mepEnPesos = np.nan
    try:
        for e in body:
            if 'DOLAR MEP' in e['especie']:
                dolares.append(float(e['ultimo']))
        mepEnPesos = sum(dolares) / len(dolares)
    except Exception as err:
        pass

    return mepEnPesos


async def preciosRava(ticker: str):
    return await precioMep() if ticker.upper() == 'MEP' else await precioEspecie(ticker)

