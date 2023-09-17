import pandas as pd
import matplotlib.pyplot as plt

def transform_ba37d():
    df = pd.read_csv('datos/flujoFondos_BA37D.csv')
    df = df[['Fecha de pago', 'Renta', 'Amortización', 'R+A']]
    df = df.rename({'Fecha de pago': 'FECHA', 'Renta': 'CUPÓN', 'Amortización': 'AMORTIZACIÓN', 'R+A': 'TOTAL'}, axis=1)
    total = df.TOTAL.sum()
    df['SALDO'] = 0
    df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d/%m/%Y").dt.date
    df = df[['FECHA', 'SALDO', 'CUPÓN', 'AMORTIZACIÓN', 'TOTAL']]
    df['ticker'] = 'BA37D'

    return df

years =[(29,1), (30,1), (35,1), (38,1), (41,1), (46,1)]
keys = ['SALDO', 'CUPÓN', 'AMORTIZACIÓN', 'TOTAL']
flujos = transform_ba37d()
for e in years:
    year = e[0]
    bond = f"AL{year}D" if year != 38 else f'AE{year}D'
    bond = f"GD{year}D" if year == 46 else bond
    url = f"https://bonistas.com/bonos-argentinos/{bond}"
    df_flujo = pd.read_html(url)[3]
    df_flujo["FECHA"] = pd.to_datetime(df_flujo["FECHA"], format="%Y/%m/%d").dt.date

    # print(df_flujo.tail())


    df_flujo[keys] = e[1] * df_flujo[keys]
    df_flujo["ticker"] = bond

    flujos = pd.concat([flujos, df_flujo])

print(flujos.head())

agg = flujos[['FECHA', 'TOTAL']].groupby('FECHA').agg('sum')

print(agg.head(50))
fig = plt.figure(figsize = (10, 5))

labels =  [str(e) for e in agg.index]
plt.bar(labels[:10], agg.TOTAL[:10], label=labels, width=.6, color='orange')
plt.show()
