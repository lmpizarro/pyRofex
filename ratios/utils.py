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

