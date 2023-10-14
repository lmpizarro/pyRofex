import pandas as pd
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from utils import change_index
from datetime import datetime, timedelta
from rava import ultima_coti_bono_mep

from dataclasses import dataclass

keys = ['FECHA', 'SALDO', 'CUPÓN', 'AMORTIZACIÓN', 'TOTAL']
def flujo_ba37d():
    df = pd.read_csv('datos/flujoFondos_BA37D.csv')
    df = df[['Fecha de pago', 'Renta', 'Amortización', 'R+A']]
    df = df.rename({'Fecha de pago': 'FECHA', 'Renta': 'CUPÓN', 'Amortización': 'AMORTIZACIÓN', 'R+A': 'TOTAL'}, axis=1)

    df["acumulado"] = df.TOTAL.cumsum()
    total = df.TOTAL.sum()
    df['SALDO'] = 0
    df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d/%m/%Y").dt.date
    df = df[keys]
    df['ticker'] = 'BA37D'

    buy_date = datetime.now().date()
    # df = change_index(df, key='FECHA')
    df = df[df.FECHA > buy_date]

    ult_precio = ultima_coti_bono_mep()
    data = {'SALDO': 0, 'CUPÓN': -ult_precio, 'AMORTIZACIÓN': 0, 'TOTAL': -ult_precio, 'ticker': 'BA37D'}
    df = pd.concat([pd.DataFrame(data=data, index=[buy_date+timedelta(days=2)]), df])
    df = df[['ticker']+keys]
    df['acumulado'] = df.TOTAL.cumsum()
    print(ult_precio)
    return df


@dataclass
class BonoArg:
    precio: float
    ticker: str
    paridad: str
    vt: str
    tir: str
    md: str
    # flujos: pd.DataFrame

def get_other_values(soup):
    values = {}
    maps_variables = {'precio': 1, 'ticker': 0, 'paridad': 3, 'vt': 4, 'tir': 5, 'md': 6}
    for k, v in maps_variables.items():
        values[k] = soup[0].iloc[v]['Valor']
    return BonoArg(**values)

def flujo_bono_soberano(year):
    ticker_for_query = f"AL{year}D" if year != 38 else f'AE{year}D'
    ticker_for_query = f"GD{year}D" if year == 46 else ticker_for_query
    url = f"https://bonistas.com/bonos-argentinos/{ticker_for_query}"
    soup = pd.read_html(url)
    df_flujo = soup[3]
    df_flujo["FECHA"] = pd.to_datetime(df_flujo["FECHA"], format="%Y/%m/%d").dt.date
    ult_precio = -float(soup[0].iloc[1]['Valor'])
    buy_date =datetime.now().date()
    line = dict(zip(keys, [buy_date+timedelta(days=2), 0, ult_precio, 0, ult_precio] ))
    line_df = pd.DataFrame.from_records([line])
    df_flujo = pd.concat([line_df, df_flujo])
    df_flujo["ticker"] = ticker_for_query
    df_flujo = df_flujo[['ticker']+ keys]
    df_flujo['acumulado'] = df_flujo['TOTAL'].cumsum()

    print(df_flujo[df_flujo['acumulado'] > 0].head(1))
    print(ult_precio)

    return df_flujo

def main():
    years =[29, 30, 35, 38, 41, 46]
    df_flujo = flujo_ba37d()
    print(df_flujo[df_flujo['acumulado'] > 0].head(1))
    flujos = df_flujo
    for year in years:

        df_flujo = flujo_bono_soberano(year=year)
        flujos = pd.concat([flujos, df_flujo])

    # print(flujos.head())

    agg = flujos[['FECHA', 'TOTAL']].groupby('FECHA').agg('sum')

    # print(agg.head(50))
    fig = plt.figure(figsize = (10, 5))

    labels =  [str(e) for e in agg.index]
    plt.bar(labels[:10], agg.TOTAL[:10], label=labels, width=.6, color='orange')
    plt.show()


# df = transform_ba37d()

# print(df.head(14))

if __name__ == '__main__':
    main()