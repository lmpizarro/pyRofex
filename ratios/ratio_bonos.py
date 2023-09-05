import pandas as pd
from pathlib import Path


FORMAT_FILENAME = "{0}D - Cotizaciones historicas.csv"
DATA_PATH = "datos"

def change_index(df_bono: pd.DataFrame) -> pd.DataFrame:
    df_bono["Fecha"] = pd.to_datetime(df_bono["fecha"], format="%Y-%m-%d").dt.date
    df_bono.set_index("Fecha", inplace=True)
    df_bono.drop(['fecha'], axis=1)
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
    def read_bono_al(year:int) -> pd.DataFrame:
        key_al = CSVS.get_key_al(year=year)
        filename_al = FORMAT_FILENAME.format(key_al)
        filename_al = Path(DATA_PATH) / filename_al
        print(filename_al)
        df_al = CSVS.read_bono(filename=filename_al)

        return df_al


    @staticmethod
    def read_bono_gd(year:int):
        key_gd = CSVS.get_key_gd(year)
        filename_gd = FORMAT_FILENAME.format(key_gd)
        filename_gd = Path(DATA_PATH) / filename_gd
        print(filename_gd)
        df_gd = CSVS.read_bono(filename=filename_gd)
        return  df_gd

def regressor(df_al_gd: pd.DataFrame):
    x = df_al_gd.index
    y = df_al_gd.ratio
    from scipy import stats

    slope, intercept, r, p, std_err = stats.linregress(x, y)

    def myfunc(x):
        return slope * x + intercept

    regress = list(map(myfunc, x))
    return x, y, regress

def calc_ratio(df_gd, df_al):
    df_al_gd  = df_al.merge(df_gd, left_on='fecha', right_on='fecha', suffixes=('_al', '_gd'))
    df_al_gd['ratio'] = df_al_gd['cierre_gd'] / df_al_gd['cierre_al']
    mean_ratio = df_al_gd.ratio.mean()

    x, y, regres = regressor(df_al_gd=df_al_gd)

    df_al_gd['regres'] = regres
    df_al_gd['mean_ratio'] = mean_ratio

    return df_al_gd[['regres', 'ratio', 'fecha', 'cierre_gd', 'cierre_al', 'mean_ratio', 'especie_al', 'especie_gd']]

def plot_them(df_al_gd):
    print(df_al_gd.tail())

    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 5.7), layout='constrained')

    ax.plot(df_al_gd.index, df_al_gd.ratio)
    ax.plot(df_al_gd.index, df_al_gd.regres)
    ax.plot(df_al_gd.index, df_al_gd.mean_ratio)
    ax.set_title(f'ratio {df_al_gd.especie_gd[0]} {df_al_gd.especie_al[0]}')
    ax.legend(['ratio', 'regresion', 'media'])
    plt.show()

def calc_ratio_bono(year=29):
    df_gd = CSVS.read_bono_gd(year=year)
    df_al = CSVS.read_bono_al(year=year)

    df_al_gd = calc_ratio(df_gd=df_gd, df_al=df_al)

    return df_al_gd

def calc_list_bonos(years=[29, 30, 35, 38, 41]):
    ratios = {}
    for year in years:
        ratios[year] = calc_ratio_bono(year=year)
    return ratios

def get_plotly_fig(df_ratio):

    import plotly.express as px
    import plotly.graph_objects as go

    df_ratio["fecha"] = pd.to_datetime(df_ratio["fecha"], format="%Y-%m-%d").dt.date

    bonds = f"{df_ratio['especie_al'][0]}/{df_ratio['especie_al'][0]}"

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df_ratio.fecha, y=df_ratio.ratio, name=f'ratio {bonds}'))
    fig.add_trace(go.Scatter(x=df_ratio.fecha, y=df_ratio.regres, name=f'regres {bonds}'))
    fig.add_trace(go.Scatter(x=df_ratio.fecha, y=df_ratio.mean_ratio, name=f'mean {bonds}'))

    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.0, y=1.05,
                            xanchor='left', yanchor='bottom',
                            text=f'Ratios for bonds {bonds}',
                            font=dict(family='Arial',
                                        size=30,
                                        color='rgb(37,37,37)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)
    return fig

def main():
    years =[29, 30, 35, 38, 41]
    ratios = calc_list_bonos(years=years)
    for year, df_ratio in ratios.items():
        plot_them(df_ratio)

        fig = get_plotly_fig(df_ratio=df_ratio)
        fig.show()

if __name__ == "__main__":
    main()