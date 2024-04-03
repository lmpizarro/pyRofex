from rava import coti_hist, scrap_bonos_rava
from utils import change_index
import matplotlib.pyplot as plt
import yfinance as yf
from variables_bcra import variables_bcra
import pandas as pd

def ratioPasesMinor():
    dfMinor = variables_bcra(tipo="minorista", desde='2010-01-31')
    dfPases = variables_bcra(tipo="pasesPasivos")

    df  = dfMinor.merge(dfPases, left_index=True, right_index=True)

    df['ratio'] = df['pasesPasivos'] / df['minorista']

    plt.plot(df['ratio'])
    plt.title('pases pasivos expresado como  Dolar Minorista')
    plt.grid()
    plt.show()

def ratioMepMinor():

    dfMinor = variables_bcra(tipo="minorista", desde='2010-01-31')
    dfMep = coti_hist(scrap_bonos_rava("DOLAR MEP"))[['fecha', 'ultimo']]
    dfMep = dfMep.rename({'ultimo': 'mep'}, axis=1)
    dfMep['mep'] = dfMep['mep'].astype(float)
    dfMinor['fecha'] = dfMinor.index
    dfMinor['fecha'] = dfMinor['fecha'].astype(str)

    df  = dfMinor.merge(dfMep, left_on='fecha', right_on='fecha', suffixes=('_cer', f'_mep'))

    df['ratio'] = df['mep'] / df['minorista']
    df['brecha'] = (df['mep'] / df['minorista']) - 1

    df = change_index(df)

    mean = df.ratio.mean()

    plt.plot(df['ratio']/mean)
    plt.axhline(y=1, color = 'r')
    plt.title('ratio Dolar MEP  Dolar Minorista')
    plt.grid()
    plt.show()

    mean = df.brecha.mean()
    plt.plot(df['brecha'])
    plt.axhline(y=mean, color = 'r')
    plt.title('brecha Dolar MEP  Dolar Minorista')
    plt.grid()
    plt.show()

def ratioBlendCer(alpha=.20):
    dfMinor = variables_bcra(tipo="minorista", desde='2010-01-31')
    dfMep = coti_hist(scrap_bonos_rava("DOLAR MEP"))[['fecha', 'ultimo']]
    dfMep = dfMep.rename({'ultimo': 'mep'}, axis=1)
    dfMep['mep'] = dfMep['mep'].astype(float)
    dfMinor['fecha'] = dfMinor.index
    dfMinor['fecha'] = dfMinor['fecha'].astype(str)

    df  = dfMinor.merge(dfMep, left_on='fecha', right_on='fecha', suffixes=('_min', f'_mep'))
    df['blend'] = (1-alpha)*df['minorista'] + alpha * df['mep']
    df = df[['blend', 'fecha']]

    dfCer = variables_bcra()
    dfCer['fecha'] = dfCer.index
    dfCer['fecha'] = dfCer['fecha'].astype(str)

    df  = dfCer.merge(df, left_on='fecha', right_on='fecha', suffixes=('_cer', f'_mep'))

    print(df.tail())
    df['ratio'] = df['blend'] / df['cer']
    df = change_index(df)

    mean = df.ratio.mean()

    plt.plot(df['ratio']/mean)
    plt.axhline(y=1, color = 'r')
    plt.title('ratio Dolar BLEND  cer')
    plt.grid()
    plt.show()



def ratioMepCer():
    dfCer = variables_bcra()
    dfCer['fecha'] = dfCer.index
    dfCer['fecha'] = dfCer['fecha'].astype(str)

    dfMep = coti_hist(scrap_bonos_rava("DOLAR MEP"))[['fecha', 'ultimo']]
    dfMep = dfMep.rename({'ultimo': 'mep'}, axis=1)
    dfMep['mep'] = dfMep['mep'].astype(float)

    df  = dfCer.merge(dfMep, left_on='fecha', right_on='fecha', suffixes=('_cer', f'_mep'))
    df['ratio'] = df['mep'] / df['cer']
    df = change_index(df)

    mean = df.ratio.mean()

    plt.plot(df['ratio']/mean)
    plt.axhline(y=1, color = 'r')
    plt.title('ratio Dolar MEP  cer')
    plt.grid()
    plt.show()


def ratiosBonoCerCer():
    dfCer = variables_bcra()
    dfCer['fecha'] = dfCer.index

    for bono in ['cuap', 'dicp', 'dip0', 'parp', 'pap0']:
        dfBono = coti_hist(scrap_bonos_rava(bono))[['fecha', 'cierre']]
        dfBono = dfBono.rename({'cierre': bono}, axis=1)
        dfBono[bono] = dfBono[bono].astype(float)
        dfCer['fecha'] = dfCer['fecha'].astype(str)
        df  = dfCer.merge(dfBono, left_on='fecha', right_on='fecha', suffixes=('_cer', f'_{bono}'))
        df = change_index(df)
        df['ratio'] = df[f'{bono}'] / df['cer']
        mean = df.ratio.mean()

        plt.plot(df['ratio']/mean)
        plt.axhline(y=1, color = 'r')
        plt.title(f'{bono} / cer')
        plt.grid()
        plt.show()


def ratiosBonoCerMep():
    dfMep = coti_hist(scrap_bonos_rava("DOLAR MEP"))[['fecha', 'ultimo']]
    dfMep = dfMep.rename({'ultimo': 'mep'}, axis=1)
    dfMep['mep'] = dfMep['mep'].astype(float)


    for bono in ['cuap', 'dicp', 'dip0', 'parp', 'pap0']:
        dfBono = coti_hist(scrap_bonos_rava(bono))[['fecha', 'cierre']]
        dfBono = dfBono.rename({'cierre': bono}, axis=1)
        dfBono[bono] = dfBono[bono].astype(float)
        df  = dfMep.merge(dfBono, left_on='fecha', right_on='fecha', suffixes=('_mep', f'_{bono}'))

        df = change_index(df)
        df['ratio'] = df[f'{bono}'] / df['mep']
        mean = df.ratio.mean()

        print(df.columns)

        plt.plot(df['ratio']/mean)
        plt.axhline(y=1, color = 'r')
        plt.title(f'{bono} / mep')
        plt.grid()
        plt.show()

def emergent(start="2015-01-01"):
    tickers = ["EEM", "EWZ", 'SPY', 'EMB', 'TLT', 'IWM', 'DIA'] # '^TNX'
    tickers = ["XOM", "CVX", "YPF", 'SHEL', "SPY", "DIA", "IWM"]
    df = yf.download(tickers, start=start, auto_adjust=True)["Close"]

    return df




if __name__ == "__main__":
    ratioBlendCer()
    ratioPasesMinor()
    ratioMepMinor()
    ratioMepCer()
    ratiosBonoCerCer()
    exit()
    ratiosBonoCerMep()
    exit()
    df = emergent()

    ratios = [(c, e) for i,c in enumerate(df.columns) for e in df.columns[i+1:]]


    for pratio in ratios:
        ratio = f'{pratio[0]}:{pratio[1]}'
        df[ratio] = df[pratio[0]] / df[pratio[1]]
        mean = df[ratio].mean()

        # plt.plot(df[ratio]/mean)
        # plt.axhline(y=1, color = 'r')
        # plt.grid()
        # plt.title(f'{ratio}')
        # plt.show()

    fig, axs = plt.subplots(3, 7)
    j = 0
    for i in range(len(ratios)):
        if not i%7:
            j += 1
        # print(j-1, i%7)
        ratio = f'{ratios[i][0]}:{ratios[i][1]}'
        mean = df[ratio].mean()
        axs[j-1, i%7].plot(df[ratio]/mean)
        axs[j-1, i%7].axhline(y=1, linestyle='--')
        axs[j-1, i%7].set_title(ratio)
        axs[j-1, i%7].grid()
    for ax in axs.flat:
        ax.label_outer()
    plt.show()
    exit()



