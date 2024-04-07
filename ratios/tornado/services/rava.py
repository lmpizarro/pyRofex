import requests
from bs4 import BeautifulSoup
import json
import numpy as np

urls = {
    "perfilRava": "https://www.rava.com/perfil",
    "dolar" : 'https://www.rava.com/cotizaciones/dolares'
}

def precioEspecie(bono='ba37d'):
    ''' devuelve la ultima cotizacion de un bono en pesos expresado en dolar'''
    url = f'https://www.rava.com/perfil/{bono}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    table = soup.find("main").find("perfil-p")
    last = np.nan
    try:
        return float(json.loads(table.attrs[':res'])['cuad_tecnico'][0]['ultimonum'])
    except:
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

