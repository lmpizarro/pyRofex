from pathlib import Path
import pandas as pd


FORMAT_FILENAME = "{0}{1} - Cotizaciones historicas.csv"
DATA_PATH = "datos"

def change_index(df_bono: pd.DataFrame, key='fecha') -> pd.DataFrame:
    df_bono["Fecha"] = pd.to_datetime(df_bono[key], format="%Y-%m-%d").dt.date
    df_bono.set_index("Fecha", inplace=True)
    df_bono.drop([key], axis=1, inplace=True)
    return df_bono

class CSVS:
    @staticmethod
    def read_bono(filename):
        df_bono = pd.read_csv(filename)
        return df_bono

    @staticmethod
    def get_key_al(year: int) -> str:
        return (f"al{year}" if year != 38 else f"ae{year}").upper()

    @staticmethod
    def get_key_gd(year: int) -> str:
        return f"gd{year}".upper()

    @staticmethod
    def read_bono_al(year:int, D=True) -> pd.DataFrame:
        key_al = CSVS.get_key_al(year=year)
        filename_al = FORMAT_FILENAME.format(key_al, 'D' if D else '')
        filename_al = Path(DATA_PATH) / filename_al
        print(filename_al)
        df_al = CSVS.read_bono(filename=filename_al)

        return df_al


    @staticmethod
    def read_bono_gd(year:int, D=True):
        key_gd = CSVS.get_key_gd(year)
        filename_gd = FORMAT_FILENAME.format(key_gd, 'D' if D else '')
        filename_gd = Path(DATA_PATH) / filename_gd
        print(filename_gd)
        df_gd = CSVS.read_bono(filename=filename_gd)
        return  df_gd

    @staticmethod
    def read_bono_ba37d():
        filename = FORMAT_FILENAME.format('BA', '37D')
        filename = Path(DATA_PATH) / filename
        df = CSVS.read_bono(filename=filename)
        return df

def regressor(df_al_gd: pd.DataFrame, key='ratio'):
    x = df_al_gd.index
    y = df_al_gd[key]
    from scipy import stats

    slope, intercept, r, p, std_err = stats.linregress(x, y)

    def regress_func(x):
        return slope * x + intercept

    regress = list(map(regress_func, x))
    return x, y, regress

def genDates():
    import calendar
    import datetime
    from datetime import timedelta
    import yfinance as yf
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    assets = {'SPY':{'colour': 'g-'}, 'AAPL':{'colour': 'ko-'}, 'TSLA':{'colour': 'rx-'}}
    colours = {'AAPL': 'rx-', 'TSLA': 'ko-', 'SPY': 'g-'}

    print(calendar.monthrange(2023, 12))
    today = datetime.datetime.now().date()
    sixmonths = timedelta(days=180)

    endDates = [(datetime.date(y, m, calendar.monthrange(y, m)[1]) - sixmonths, datetime.date(y, m, calendar.monthrange(y, m)[1]))  for y in range(2011, 2025) for m in range(1, 13) if datetime.date(y, m, calendar.monthrange(y, m)[1]) < today]
    df = yf.download(list(assets.keys()), start=endDates[0][0])['Adj Close']
    returns = np.log(df/df.shift(1))
    stds = pd.DataFrame()
    for rng in endDates:
        sdf = returns.loc[rng[0]:rng[1]]
        meanD = {}
        for asset in assets:
            meanD['asset'] = asset
            meanD['mean']  = sdf[asset].mean()
            meanD['std']   = sdf[asset].std()
            meanD['date'] = rng[1]
            df2 =pd.DataFrame.from_dict([meanD])
            stds = pd.concat([stds, df2 ], ignore_index=True)
    for asset in assets:
        assetdata = stds[stds.asset==asset].set_index('date')
        plt.plot(assetdata['std'], assets[asset]['colour'])
    plt.show()
genDates()


