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
        soup[0].iloc[4]['Descripción']: float(filterNum(soup[0].iloc[4].Valor)),
        soup[0].iloc[5]['Descripción']: float(filterNum(soup[0].iloc[5].Valor)),
        soup[0].iloc[6]['Descripción']: float(filterNum(soup[0].iloc[6].Valor)),
        soup[1].iloc[0]['Métricas']: float(filterNum(soup[1].iloc[0].Valor)),
        soup[1].iloc[1]['Métricas']: float(filterNum(soup[1].iloc[1].Valor)),
        soup[1].iloc[2]['Métricas']: float(filterNum(soup[1].iloc[2].Valor)),
        soup[1].iloc[3]['Métricas']: float(filterNum(soup[1].iloc[3].Valor)),
        soup[1].iloc[4]['Métricas']: float(filterNum(soup[1].iloc[4].Valor)),
           }

    return df_flujo, datos



if __name__ == '__main__':
    flujos = {}
    datos_adicionales = []
    for bono in ['DIP0', 'CUAP', 'PAP0', 'PARP', 'DICP']:

        url = f"https://bonistas.com/bonos-argentinos/{bono}"

        df, other_datos = bonistas(bono)
        datos_adicionales.append(other_datos)
        print(df.tail())
        # print(df['ticker'].iloc[0], 100*df['returns'][1:].mean(), df['TOTAL'][1:].sum()/df['TOTAL'].iloc[0])

        flujos[bono] = df
    plot_cash_flow_all(flujos)

    plot_cash_flow_all(flujos, 'returns')

    df_datos = pd.DataFrame.from_records(datos_adicionales)

    print(df_datos)


