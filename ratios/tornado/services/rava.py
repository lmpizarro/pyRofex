import requests
from bs4 import BeautifulSoup
import json
import numpy as np

urls = {
    "perfilRava": "https://www.rava.com/perfil",
    "dolar" : 'https://www.rava.com/cotizaciones/dolares'
}

class Asset:
    def __init__(self, ticker=None, price=None) -> None:
        self.ticker = ticker
        self.price = price

def precioEspecie(ticker='ba37d'):
    ''' last price & properties '''
    url = f'https://www.rava.com/perfil/{ticker}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

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

def precioMep():
    url = urls['dolar']
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
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


def preciosRava(ticker: str):
    return precioMep() if ticker.upper() == 'MEP' else precioEspecie(ticker)

