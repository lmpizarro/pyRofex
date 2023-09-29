from utils import CSVS, change_index, regressor
from dolares import dolar_ccl, dolar_mep
from variables_bcra import variables_bcra
import pandas as pd
import matplotlib.pyplot as plt


def main():
    df = CSVS.read_bono_ba37d()
    df = change_index(df)[['cierre', 'volumen']]
    df_ccl = dolar_ccl()[['ccl', 'cclars']]
    df_mep = dolar_mep()
    df_cer = variables_bcra(tipo="cer", desde="2015-01-01")

    df_merge  = pd.merge(df, df_ccl,  right_index=True, left_index=True)
    df_merge  = pd.merge(df_merge, df_mep,  right_index=True, left_index=True)
    df_merge  = pd.merge(df_merge, df_cer,  right_index=True, left_index=True)
    df_merge['close_ccl'] = df_merge.cierre / df_merge.ccl
    df_merge['close_mep'] = df_merge.cierre / df_merge.mep
    df_merge['rBa37DCer'] = df_merge.cierre / df_merge.cer
    df_merge['rBa37DCclCer'] = df_merge.close_mep / df_merge.cer

    from scipy import stats


    def regress_func(key):
        x = range(len(df_merge.index))
        slope, intercept, _, _, _ = stats.linregress(x,
                                                    df_merge[key])
        return slope * x + intercept

    df_merge['regress'] = regress_func('close_mep')


    print(df.tail())
    print(df_ccl.tail())
    print(df_merge.tail())
    print('mean: ', df_merge.close_mep.mean())
    print('close: ', df_merge.close_mep.iloc[-1])

    # plt.plot(df_merge.close_ccl)
    plt.plot(df_merge.close_mep, 'k')
    plt.plot(df_merge.regress)
    plt.axhline(y=df_merge.close_mep.mean(), color = 'y')
    plt.axhline(y=df_merge.close_mep.mean() + df_merge.close_mep.std(), color = 'g')
    plt.axhline(y=df_merge.close_mep.mean() - df_merge.close_mep.std(), color = 'r')
    plt.show()

    plt.plot(df_merge.rBa37DCclCer - df_merge.rBa37DCclCer.mean(), 'k')
    plt.axhline(y=0, color = 'r')
    plt.show()

    plt.plot(df_merge.rBa37DCer - df_merge.rBa37DCer.mean(), 'k')
    plt.axhline(y=0, color = 'r')
    plt.show()


if __name__ == '__main__':
    main()