import pandas as pd
import matplotlib.pyplot as plt

from utils import regressor, CSVS, change_index

def calc_ratio_gd_al(df_gd, df_al):
    df_al_gd  = df_al.merge(df_gd, left_on='fecha', right_on='fecha', suffixes=('_al', '_gd'))
    df_al_gd['ratio'] = df_al_gd['cierre_gd'] / df_al_gd['cierre_al']
    mean_ratio = df_al_gd.ratio.mean()

    x, y, regres = regressor(df_al_gd=df_al_gd)

    df_al_gd['regres'] = regres
    df_al_gd['mean_ratio'] = mean_ratio

    return df_al_gd[['regres', 'ratio', 'fecha', 'cierre_gd', 'cierre_al', 'mean_ratio', 'especie_al', 'especie_gd']]

def plot_them(df_al_gd):
    print(df_al_gd.tail())

    fig, ax = plt.subplots(figsize=(10, 5.7), layout='constrained')

    ax.plot(df_al_gd.index, df_al_gd.ratio)
    ax.plot(df_al_gd.index, df_al_gd.regres)
    ax.plot(df_al_gd.index, df_al_gd.mean_ratio)
    ax.set_title(f'ratio {df_al_gd.especie_gd[0]} {df_al_gd.especie_al[0]}')
    ax.legend(['ratio', 'regresion', 'media'])
    plt.show()

def calc_ratio_bono(year=29, D=True):
    df_gd = CSVS.read_bono_gd(year=year, D=D)
    df_al = CSVS.read_bono_al(year=year, D=D)

    df_al_gd = calc_ratio_gd_al(df_gd=df_gd, df_al=df_al)

    return df_al_gd

def calc_list_bonos(years=[29, 30, 35, 38, 41], D=True):
    ratios = {}
    for year in years:
        ratios[year] = calc_ratio_bono(year=year, D=D)
    return ratios

def get_plotly_fig(df_ratio):

    import plotly.express as px
    import plotly.graph_objects as go

    df_ratio["fecha"] = pd.to_datetime(df_ratio["fecha"], format="%Y-%m-%d").dt.date

    bonds = f"{df_ratio['especie_gd'][0]}/{df_ratio['especie_al'][0]}"

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
    ratios = calc_list_bonos(years=years, D=False)
    for year, df_ratio in ratios.items():
        plot_them(df_ratio)

        # fig = get_plotly_fig(df_ratio=df_ratio)
        # fig.show()

def mep_bono(year=29):
    df_al_D = CSVS.read_bono_al(year=year, D=True)
    df_al_P = CSVS.read_bono_al(year=year, D=False)

    df_al_D = df_al_D[['fecha', 'cierre']]
    df_al_P = df_al_P[['fecha', 'cierre']]

    df_al_gd  = df_al_D.merge(df_al_P, left_on='fecha', right_on='fecha', suffixes=('_d', '_p'))
    df_al_gd['mep'] = df_al_gd['cierre_p'] / df_al_gd['cierre_d']

    x, y, regres = regressor(df_al_gd=df_al_gd, key='mep')

    df_al_gd['regres'] = regres

    df_al_gd = change_index(df_al_gd)

    return df_al_gd


def ratio_37_46():
    mep_al30 = mep_bono(30)['mep']
    gd46d = change_index(CSVS.read_bono_gd(38))
    ba37d = change_index(CSVS.read_bono_ba37d())

    df = pd.merge(mep_al30, ba37d, left_index=True, right_index=True)
    df = pd.merge(df, gd46d, left_index=True, right_index=True, suffixes=['37', '46'])
    print(df.tail())
    df['close37'] = df['cierre37'] / df['mep']
    df['ratio'] = df['close37'] / df['cierre46']
    df['ratiomean'] = df.ratio.mean()


    plt.plot(df.index, df.close37)
    plt.plot(df.index, df.cierre46)
    plt.show()
    plt.plot(df.index, 2 * (df.close37 - df.cierre46)/ (df.close37+df.cierre46))

    plt.show()


    plt.plot(df.index, df.ratio-1)
    plt.plot(df.index, df.ratiomean-1)
    plt.plot(df.index, df.ratiomean-1 + (df.ratio-1).std())
    plt.plot(df.index, df.ratiomean-1 - (df.ratio-1).std())
    plt.show()

    df[['close37', 'cierre46', 'ratio', 'ratiomean']].to_csv('ratios3746.csv')

if __name__ == "__main__":
    main()
    # ratio_37_46()

