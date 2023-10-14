import pandas as pd
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from utils import change_index
from datetime import datetime, timedelta
from rava import ultima_coti_bono_mep

from dataclasses import dataclass

print('ba37d en dolares: ', ultima_coti_bono_mep())


def transform_ba37d():
    df = pd.read_csv('datos/flujoFondos_BA37D.csv')
    df = df[['Fecha de pago', 'Renta', 'Amortización', 'R+A']]
    df = df.rename({'Fecha de pago': 'FECHA', 'Renta': 'CUPÓN', 'Amortización': 'AMORTIZACIÓN', 'R+A': 'TOTAL'}, axis=1)

    df["acumulado"] = df.TOTAL.cumsum()
    total = df.TOTAL.sum()
    df['SALDO'] = 0
    df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d/%m/%Y").dt.date
    df = df[['FECHA', 'SALDO', 'CUPÓN', 'AMORTIZACIÓN', 'TOTAL']]
    df['ticker'] = 'BA37D'

    limit_date = datetime.now().date()
    df = change_index(df, key='FECHA')
    df = df[df.index > limit_date]


    data = {'SALDO': 0, 'CUPÓN': 0, 'AMORTIZACIÓN': 0, 'TOTAL': -ultima_coti_bono_mep(), 'ticker': 'BA37D'}
    df = pd.concat([pd.DataFrame(data=data, index=[limit_date+timedelta(days=2)]), df])
    df['acumulado'] = df.TOTAL.cumsum()
    return df


@dataclass
class BonoArg:
    # precio: float
    # ticker: str
    # paridad: str
    # vt: str
    # tir: str
    # md: str
    calendar: pd.DataFrame

maps_variables = {'Precio': 1, 'ticker': 0, 'Paridad': 3, 'Valor Técnico': 4, 'TIR': 5, 'MD': 6}
def main():
    years =[(29,1), (30,1), (35,1), (38,1), (41,1), (46,1)]
    keys = ['SALDO', 'CUPÓN', 'AMORTIZACIÓN', 'TOTAL']
    flujos = transform_ba37d()
    for e in years:
        year = e[0]
        bond = f"AL{year}D" if year != 38 else f'AE{year}D'
        bond = f"GD{year}D" if year == 46 else bond
        url = f"https://bonistas.com/bonos-argentinos/{bond}"
        soup = pd.read_html(url)
        df_flujo = soup[3]
        df_flujo["FECHA"] = pd.to_datetime(df_flujo["FECHA"], format="%Y/%m/%d").dt.date
        values = {}
        for k, v in maps_variables.items():
            values[k] = soup[0].iloc[v]['Valor']

        precio = -float(soup[0].iloc[1]['Valor'])
        line = dict(zip(['FECHA']+ keys, [datetime.now().date(), 0, precio, 0, precio] ))
        line_df = pd.DataFrame.from_records([line])
        df_flujo = pd.concat([line_df, df_flujo])
        df_flujo['acumulado'] = df_flujo['TOTAL'].cumsum()
        print(bond)
        print(df_flujo[df_flujo['acumulado'] > 0].head(1))

        df_flujo[keys] = e[1] * df_flujo[keys]
        df_flujo["ticker"] = bond

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