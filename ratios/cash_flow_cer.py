from rava import cash_flow_bono
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from datetime import timedelta



def plot_cash_flow_all(flujos, key='acumulado'):
    for b in flujos:
        cf = flujos[b]
        plt.grid()
        plt.plot(cf.index,  cf[key], label=b)
        plt.scatter(cf.index,  cf[key])
        plt.legend()
    plt.title('all bonds')
    plt.axhline(y=0, color = 'r')
    plt.show()

keys = ['FECHA', 'SALDO', 'CUPÓN', 'AMORTIZACIÓN', 'TOTAL']

def filterNum(string):
    return ''.join([s for s in string if s in '9678543210.'])

def bonistas(bono):
    url = f"https://bonistas.com/bonos-argentinos/{bono}"
    soup = pd.read_html(url)
    df_flujo = soup[3]
    df_flujo["FECHA"] = pd.to_datetime(df_flujo["FECHA"], format="%Y/%m/%d").dt.date
    ult_precio = float(soup[0].iloc[1]['Valor'])
    buy_date =datetime.now().date()
    liq_date = buy_date+timedelta(days=2)
    line = dict(zip(keys, [liq_date, 0, -ult_precio, 0, -ult_precio] ))
    line_df = pd.DataFrame.from_records([line])
    df_flujo = pd.concat([line_df, df_flujo])
    df_flujo["ticker"] = bono
    df_flujo = df_flujo[['ticker']+ keys]
    df_flujo['acumulado'] = df_flujo['TOTAL'].cumsum()
    df_flujo["returns"] = df_flujo["TOTAL"] / ult_precio
    df_flujo.set_index('FECHA', inplace=True)
    datos = {
        soup[0].iloc[0]['Descripción']: soup[0].iloc[0].Valor,
        soup[0].iloc[1]['Descripción']: float(filterNum(soup[0].iloc[1].Valor)),
        # soup[0].iloc[2]['Descripción']: filterNum(soup[0].iloc[2].Valor),
        soup[0].iloc[3]['Descripción']: float(filterNum(soup[0].iloc[3].Valor)),
        'VT': float(filterNum(soup[0].iloc[4].Valor)),
        soup[0].iloc[5]['Descripción']: float(filterNum(soup[0].iloc[5].Valor)),
        soup[0].iloc[6]['Descripción']: float(filterNum(soup[0].iloc[6].Valor)),
        'TIR Obj': float(filterNum(soup[1].iloc[0].Valor)),
        soup[1].iloc[1]['Métricas']: float(filterNum(soup[1].iloc[1].Valor)),
        'TIR Prom': float(filterNum(soup[1].iloc[2].Valor)),
        soup[1].iloc[3]['Métricas']: float(filterNum(soup[1].iloc[3].Valor)),
        soup[1].iloc[4]['Métricas']: float(filterNum(soup[1].iloc[4].Valor)),
        'dQ': (df_flujo.index[1] - df_flujo.index[0]).days,
        'pQ': df_flujo.iloc[1]['CUPÓN'],
        'Q/P': -df_flujo.iloc[1]['CUPÓN'] / df_flujo.iloc[0]['CUPÓN'],
        'MAT': (df_flujo.index[-1] - df_flujo.index[0]).days/365,
           }
    datos['MD/MAT'] = datos['MD'] / datos['MAT']
    datos['TIR/Prom'] = (datos['TIR'] - datos['TIR Prom']) / datos['TIR Prom']
    return df_flujo, datos



def main():
    flujos = {}
    datos_adicionales = []
    bonos_cer = ['DIP0', 'DICP', 'PAP0', 'PARP', 'CUAP']
    bonos_sob = ['AL29D', 'AL30D', 'AL35D', 'AE38D', 'AL41D', 'GD46D']
    for bono in bonos_cer:


        df, other_datos = bonistas(bono)
        datos_adicionales.append(other_datos)
        print(df.head())
        # print(df['ticker'].iloc[0], 100*df['returns'][1:].mean(), df['TOTAL'][1:].sum()/df['TOTAL'].iloc[0])

        flujos[bono] = df
    plot_cash_flow_all(flujos)

    plot_cash_flow_all(flujos, 'returns')

    df_datos = pd.DataFrame.from_records(datos_adicionales)

    df_datos.to_csv('datos.csv')


if __name__ == '__main__':
    main()
