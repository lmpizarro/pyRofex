import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

from variables_bcra import variables_bcra
from dolares import dolar_ccl, dolar_mep

def indice_merval(start="2015-01-01"):  # to be deleted
    # log_return = np.log(vfiax_monthly.open / vfiax_monthly.open.shift())

    tickers = ["ARS=X", "M.BA"]
    df_close = yf.download(tickers, start=start, auto_adjust=True)["Close"]
    df_close.dropna(inplace=True)

    # df_close["pct_change"] = (1.0 + df_close["M.BA"].pct_change())
    # df_close["ret"] = df_close["pct_change"].cumprod()
    # df_close["date"] = df_close.index

    df_close["MervARS=X"] = df_close["M.BA"] / df_close["ARS=X"]

    # df_close.dropna(inplace=True)

    # df_monthly = df_close.resample('M')["M.BA"].sum().to_frame()

    # df_monthly = df_close.loc[df_close.groupby(pd.Grouper(key='date', freq='1M')).date.idxmax()]

    return df_close[["M.BA", "MervARS=X"]]



if __name__ == "__main__":
    dfLeliq = variables_bcra(tipo="leliq", desde="2015-01-01")
    dfCER = variables_bcra(tipo="cer", desde="2015-01-01")
    dfMayorista = variables_bcra(tipo="mayorista", desde="2015-01-01")
    dfCcl = dolar_ccl()
    dfMep = dolar_mep()

    print(dfLeliq.tail())


    dfLeliqCer = pd.merge(dfCER, dfLeliq, left_index=True, right_index=True)
    dfLeliqCer = pd.merge(dfLeliqCer, dfCcl, left_index=True, right_index=True)
    dfLeliqCer["rLeliqCER"] = dfLeliqCer.leliq / dfLeliqCer.cer
    dfLeliqCer["rLeliqCCL"] = dfLeliqCer.leliq / dfLeliqCer.ccl

    plt.plot(dfLeliqCer.rLeliqCCL)
    plt.show()

    dfMayCer = pd.merge(dfMayorista, dfCER, left_index=True, right_index=True)
    dfMayCer = pd.merge(dfMayCer, dfCcl, left_index=True, right_index=True)
    dfMayCer = pd.merge(dfMayCer, dfMep, left_index=True, right_index=True)
    dfMayCer['MerCcl'] = dfMayCer['M.BA'] / dfMayCer['ccl']

    dfMayCer['rMayCer'] = dfMayCer['mayorista'] / dfMayCer['cer']
    dfMayCer['rCclCer'] = dfMayCer['ccl'] / dfMayCer['cer']

    dfMayCer['rMerARSCer'] = dfMayCer['M.BA'] / dfMayCer['cer']
    dfMayCer['rMerCclCer'] = dfMayCer['MerCcl'] / dfMayCer['cer']

    dfMayCer['rGGALCer'] = dfMayCer['GGAL'] / dfMayCer['cer']
    dfMayCer['rGGALBACer'] = dfMayCer['GGAL.BA'] / dfMayCer['cer']

    dfMayCer['rYPFCer'] = dfMayCer['YPF'] / dfMayCer['cer']
    dfMayCer['rYPFBACer'] = dfMayCer['YPFD.BA'] / dfMayCer['cer']

    dfMayCer['rPAMPCer'] = dfMayCer['PAM'] / dfMayCer['cer']
    dfMayCer['rPAMPBACer'] = dfMayCer['PAMP.BA'] / dfMayCer['cer']


    dfMayCer = dfMayCer.truncate(before="2019-12-30")
    print(dfMayCer.keys())

    figure, axis = plt.subplots(2, 1)

    axis[0].plot(dfMayCer.rMayCer)
    axis[0].axhline(y=dfMayCer.rMayCer.mean(), color = 'r')
    axis[0].set_title("Mayorista/CER")

    axis[1].plot(dfMayCer.rCclCer)
    axis[1].axhline(y=dfMayCer.rCclCer.mean(), color = 'g')
    axis[1].set_title("CCL/CER")
    plt.show()

    figure, axis = plt.subplots(2, 1)
    axis[0].plot(dfMayCer.rMerARSCer)
    axis[0].axhline(y=dfMayCer.rMerARSCer.mean(), color = 'g')
    axis[0].set_title("MervalARS/CER")

    axis[1].plot(dfMayCer.rMerCclCer)
    axis[1].axhline(y=dfMayCer.rMerCclCer.mean(), color = 'y')
    axis[1].set_title("MervalCCL/CER")
    plt.show()


    # #
    figure, axis = plt.subplots(2, 1)
    axis[0].plot(dfMayCer.rGGALCer)
    axis[0].axhline(y=dfMayCer.rGGALCer.mean(), color = 'g')
    axis[0].set_title("GGAL USA/CER")
    axis[1].plot(dfMayCer.rGGALBACer)
    axis[1].axhline(y=dfMayCer.rGGALBACer.mean(), color = 'g')
    axis[1].set_title("GGAL BA/CER")


    plt.show()

    figure, axis = plt.subplots(2, 1)

    axis[0].plot(dfMayCer.rYPFCer)
    axis[0].axhline(y=dfMayCer.rYPFCer.mean(), color = 'y')
    axis[0].set_title("YPF USA/CER")


    axis[1].plot(dfMayCer.rYPFBACer)
    axis[1].axhline(y=dfMayCer.rYPFBACer.mean(), color = 'y')
    axis[1].set_title("YPF BA/CER")
    plt.show()

    figure, axis = plt.subplots(2, 1)
    axis[0].plot(dfMayCer.rPAMPBACer)
    axis[0].axhline(y=dfMayCer.rPAMPBACer.mean(), color = 'g')
    axis[0].set_title("PAMP BA/CER")

    axis[1].plot(dfMayCer.rPAMPCer)
    axis[1].axhline(y=dfMayCer.rPAMPCer.mean(), color = 'y')
    axis[1].set_title("PAMP USA/CER")
    plt.show()



    dfMepCcl = pd.merge(dfMep, dfCcl, left_index=True, right_index=True)
    figure, axis = plt.subplots(2, 1)
    axis[0].plot(dfMepCcl.mep)
    axis[0].plot(dfMepCcl.ccl)
    axis[0].legend(['MEP', 'CCL'])

    axis[0].set_title(" CCL & MEP")

    axis[1].plot(dfMepCcl.ccl/dfMepCcl.mep)
    axis[1].axhline(y=(dfMepCcl.ccl/dfMepCcl.mep).mean(), color = 'y')
    axis[1].set_title(" CCL / MEP")
    plt.show()

