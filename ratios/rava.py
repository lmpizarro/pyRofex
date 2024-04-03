import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import pandas as pd
from utils import change_index
import numpy as np
from pyxirr import xirr

DAYS_IN_A_YEAR = 365

urls = {
    "bonos_rava": "https://www.rava.com/perfil",
    "cedears": "https://www.rava.com/cotizaciones/cedears",
    "dolar" : 'https://www.rava.com/cotizaciones/dolares'
}

def dolar_mep_hoy():
    url = urls['dolar']
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    table = soup.find(name='dolares-p')
    body = json.loads(table.attrs[":datos"])["body"]

    dolares = []
    for e in body:
        if 'DOLAR MEP' in e['especie']:
            dolares.append(float(e['ultimo']))
    dolar = sum(dolares) / len(dolares)

    return dolar


def ultima_coti_bono_mep(bono='ba37d'):
    ''' devuelve la ultima cotizacion de un bono en pesos expresado en dolar'''
    url = f'https://www.rava.com/perfil/{bono}'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    table = soup.find("main").find("perfil-p")
    mep = dolar_mep_hoy()
    last = 0
    try:
        return float(json.loads(table.attrs[':res'])['cuad_tecnico'][0]['ultimonum']) / mep
    except:
        return last


def coti_hist(res):
    return pd.DataFrame(res["coti_hist"])

def scrap_bonos_rava(especie):
    url = f"{urls['bonos_rava']}/{especie}"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, features="html.parser")
    table = soup.find("main").find("perfil-p")

    res = json.loads(table.attrs[":res"])

    return res

def transform_ba37d_rava():

    """ "Fecha de pago" ,Bono ,Ticker ,Renta ,Amortización ,R+A   ,Moneda """
    df = pd.read_csv('datos/flujoFondos_BA37D.csv')
    df = df[['Fecha de pago', 'Renta', 'Amortización', 'R+A']]
    df = df.rename({'Fecha de pago': 'Fecha', 'Renta': 'renta', 'Amortización': 'amortizacion', 'R+A': 'cupon'}, axis=1)

    buy_date = datetime.now()
    ult_precio = ultima_coti_bono_mep()
    liq_date = buy_date + timedelta(days=2)
    data = {'cupon': -ult_precio, 'amortizacion': 0, 'ticker': 'BA37D', 'Fecha': liq_date.strftime('%d/%m/%Y')}
    df = pd.concat([pd.DataFrame.from_records([data]), df])

    df['ticker'] = 'BA37D'
    df["fecha"] = pd.to_datetime(df["Fecha"], format="%d/%m/%Y")
    df = df[df.fecha > buy_date]

    return df



def scrap_cedear_rava():
    url = urls["cedears"]
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(resp.text, features="html.parser")
    table = soup.find("main").find("cedears-p")

    body = json.loads(table.attrs[":datos"])["body"]

    return [b["simbolo"] for b in body]


def cash_flow(flujo):
    today = datetime.now()
    flujo.fillna(0, inplace=True)

    flujo["fecha"] = pd.to_datetime(flujo["fecha"], format="%Y-%m-%d")
    flujo["acumulado"] = flujo.cupon.cumsum()
    flujo_inicial = -flujo.acumulado.iloc[0]
    flujo["Q/P"] = flujo.cupon / flujo_inicial
    flujo["acum/P"] = flujo.acumulado / flujo_inicial
    flujo["dQ"] = (flujo.fecha - today).dt.days
    flujo['yQ'] = flujo["dQ"] / DAYS_IN_A_YEAR
    flujo = flujo.drop('dQ', axis=1)
    flujo = change_index(flujo)
    flujo['acumQ'] = flujo['acumulado'] + flujo_inicial
    flujo['acumAmort'] = flujo['amortizacion'].cumsum()
    flujo['acumRenta'] = flujo['renta'].cumsum()
    totalAmortizacion = flujo['acumAmort'].iloc[-1]
    flujo['valorResidual'] = totalAmortizacion - flujo['acumAmort']

    return flujo

def cash_flow_bono(bono):
    if bono == 'BA37D':
        flujo = transform_ba37d_rava()
    else:
        res = scrap_bonos_rava(bono)


        flujo = pd.DataFrame(res["flujofondos"]["flujofondos"])
        flujo['ticker'] = bono

        columns = ['fecha',	'renta',	'amortizacion',	'cupon','ticker']
        if bono == 'GD46D':
            data = [['2046-01-09',		0.114,	2.273,	2.386, 'GD46D'],
                    ['2046-07-10',	0.057,	2.273,	2.33, 'GD46D']]

            flujo = pd.concat([flujo, pd.DataFrame(data=data, columns=columns)])

            print(flujo.tail())



    return cash_flow(flujo)



def test():
    res = scrap_bonos_rava("gd29")

    coti_hist = pd.DataFrame(res["coti_hist"])

    print(coti_hist.head())
    flujo = pd.DataFrame(res["flujofondos"]["flujofondos"])

    dolar = res["flujofondos"]["dolar"]
    tir = res["flujofondos"]["tir"]
    duration = res["flujofondos"]["duration"]

    cf = cash_flow(flujo)

    exit()


def just_another_test():
    result = scrap_bonos_rava("TX28")
    coti_hist = coti_hist(result)

    print(coti_hist)

    cedears = scrap_cedear_rava()

    print(cedears)

    test()

def info_flujos(bono):

    cf = cash_flow_bono(bono)

    # https://anexen.github.io/pyxirr/functions.html
    tir = xirr(pd.DataFrame({"dates": cf.index, "amounts": cf['cupon']}))

    cf['factVA'] = np.power(1+tir / 2, -2*cf['yQ'])
    cf['VACashFlow'] = cf['factVA'] * cf['cupon']
    cf['VACFxT'] = cf['VACashFlow'] * cf['yQ']
    maturity = cf['yQ'].iloc[-1]
    duration =  - cf['VACFxT'][1:].sum() / cf['VACashFlow'].iloc[0]
    break_even_nominal = cf[cf['acumulado'] > 0].index[0]
    year_to_break = (break_even_nominal-datetime.today().date()).days / 365
    acumQT = cf.acumQ.iloc[-1]
    renta = acumQT - 100
    rentaY = renta / maturity
    usdY = acumQT / maturity
    precio = - cf.iloc[0].cupon
    rentaYP = rentaY / precio
    pQ = cf.iloc[1].cupon / 100
    datos = zip(('ticker', 'precio','tir', 'duration', 'ytoBrk', 'maturity', 'flujoT', 'renta', 'renta/Y', 'usd/Y', 'renta/Y/P', 'pQ', 'pQ/P'),
                (cf.ticker.iloc[0], precio, tir, duration, year_to_break, maturity, acumQT, renta, rentaY, usdY, rentaYP, pQ, 100*pQ/precio))
    dict_datos = {e[0]:e[1] for e in datos}


    return dict_datos



import requests

def getCotiHistorica(ticker):
    path = f"datos/{ticker.upper()} - Cotizaciones historicas.csv"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.rava.com/',
        'Origin': 'https://www.rava.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    data = {
        'access_token': '97619ba81e74e7405b8ad79825aec56431319b62',
        'especie': ticker,
        'fecha_inicio': '0000-00-00',
        'fecha_fin': '2024-02-03',
    }

    response = requests.post('https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos', headers=headers, data=data)
    print(response)
    df = pd.DataFrame.from_records(response.json()['body'])
    df.to_csv(path)

if __name__ == "__main__":

    #for bono in ['AL29D', 'AL30D', 'AL35D', 'AE38D', 'BA37D', 'AL41D', 'GD46D','GD30D', 'GD38D', 'GD41D', 'GD29D', 'GD35D']:
    for bono in ['AL29', 'AL30', 'AL35', 'AE38', 'AL41', 'GD46','GD30', 'GD38', 'GD41', 'GD29', 'GD35']:
        getCotiHistorica(bono)


    exit()
    dict_datos = []
    for bono in ['AL29D', 'AL30D', 'AL35D', 'AE38D', 'BA37D', 'AL41D', 'GD46D','GD30D', 'GD38D', 'GD41D', 'GD29D', 'GD35D']:

        datos = info_flujos(bono)
        dict_datos.append(datos)


    df = pd.DataFrame.from_records(dict_datos)
    df['PtomaxP'] = df['precio'] / df['precio'].max()
    df['pQ/P/meanPQ'] = df['pQ/P'] / df['pQ'].mean()
    df['renta/Y/P'] = df['renta/Y'] / df['precio']
    df['usd/Y/P'] = df['usd/Y'] / df['precio']
    df['yBrkTDur'] = df['ytoBrk'] / df['maturity']
    df = df.set_index('ticker')
    df = df.sort_values('pQ/P/meanPQ')
    # df = df.sort_values('renta/Y/P')
    # df = df.sort_values('usd/Y')
    keys1 = ['precio', 'tir', 'duration', 'ytoBrk', 'maturity', 'yBrkTDur', 'flujoT', 'usd/Y/P']
    keys2 = ['renta', 'renta/Y', 'usd/Y', 'renta/Y/P', 'pQ', 'pQ/P', 'PtomaxP', 'pQ/P/meanPQ']
    print(df[keys1])
    print(df[keys2])
