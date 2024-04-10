import requests
from bs4 import BeautifulSoup
import json
import numpy as np
import tornado

urlsBase = {
    "perfilRava": "https://www.rava.com/perfil",
    "dolar" : 'https://www.rava.com/cotizaciones/dolares'
}

def getUrlRavaPerfil(ticker):
    return  urlsBase['perfilRava']+'/'+ticker



class Asset:
    def __init__(self, ticker=None, price=None) -> None:
        self.ticker = ticker
        self.price = price


async def getResponse(url):
    ''' last price & properties '''

    response = await tornado.httpclient.AsyncHTTPClient().fetch(url)

    return response

async def precioEspecie(ticker='ba37d'):

    url = f'https://www.rava.com/perfil/{ticker}'
    response = await getResponse(url=url)
    cuadTec  = getCuadroTecnico(response=response)
    return decodeResponse(cuadTec)

def getCuadroTecnico(response):
    soup = BeautifulSoup(response.body, 'html.parser')

    try:
        table = soup.find("main").find("perfil-p")
        return  json.loads(table.attrs[':res'])['cuad_tecnico'][0]
    except:
        pass


def decodeResponse(cuadroTecnico):

    ultimoPrecio = np.nan
    try:
        varmensual = cuadroTecnico['varmensual']
        varanual = cuadroTecnico['varanual']
        especie = cuadroTecnico['especie']
        ultimoPrecio = float(cuadroTecnico['ultimonum'])
    except:
        pass

    return ultimoPrecio

async def precioMep():
    url = urlsBase['dolar']
    response = await getResponse(url=url)
    soup = BeautifulSoup(response.body, 'html.parser')
    table = soup.find(name='dolares-p')
    datos = json.loads(table.attrs[":datos"])
    datosdolares = datos["body"]

    dolaresMep = []
    mepEnPesos = np.nan

    for dolar in datosdolares:
        try:
            if 'DOLAR MEP' in dolar['especie']:
                dolaresMep.append(float(dolar['ultimo']))
        except Exception as err:
            continue
    mepEnPesos = sum(dolaresMep) / len(dolaresMep)

    return mepEnPesos


async def preciosRava(ticker: str):
    return await precioMep() if ticker.upper() == 'MEP' else await precioEspecie(ticker)

async def priceRavaList(tickers):
    return  [{'ticker': ticker, 'price': await preciosRava(ticker)}  for ticker in tickers]