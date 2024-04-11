from bs4 import BeautifulSoup
import json
import numpy as np
import tornado
from services.asyncHttpDowload import asyncFetcher

urlsBase = {
    "perfilRava": "https://www.rava.com/perfil",
    "dolar" : 'https://www.rava.com/cotizaciones/dolares'
}

def getUrlRavaPerfil(ticker):
    return  urlsBase['perfilRava']+'/'+ticker


async def getResponse(url):
    ''' last price & properties '''

    response = await tornado.httpclient.AsyncHTTPClient().fetch(url)

    return response

async def precioEspecie(ticker='ba37d'):

    url = f'https://www.rava.com/perfil/{ticker}'
    response = await getResponse(url=url)
    cuadTec  = getCuadroTecnico(response=response)
    return lastPrice(cuadTec)

def getCuadroTecnico(response):
    soup = BeautifulSoup(response.body, 'html.parser')

    table = soup.find("main").find("perfil-p")
    return  json.loads(table.attrs[':res'])['cuad_tecnico'][0]


def lastPrice(cuadroTecnico):

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

async def priceRavaList(tickers, concurrent=True):
    if not concurrent:
        return  [{'ticker': ticker, 'price': await preciosRava(ticker)}  for ticker in tickers]
    urls = [getUrlRavaPerfil(ticker=ticker) for ticker in tickers if ticker.upper() != 'MEP']
    responses = await asyncFetcher(urls=urls)
    cuadroTecnicos = [getCuadroTecnico(response['response']) for response in responses]
    return [{'especie': cuadTec['especie'], 'precio':lastPrice(cuadroTecnico=cuadTec)} for cuadTec in cuadroTecnicos]