import requests
import pandas as pd
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt

settings = {
    "cer": {"Serie": "3540", "Detalle": "CER (Base 2.2.2002=1)"},
    "badlar": {
        "Serie": "7935",
        "Detalle": "BADLAR en pesos de bancos privados (en  e.a.)",
    },
    "TEAPolMon": {
        "Serie": "7936",
        "Detalle": "Tasa de Política Monetaria (en  e.a.)",
    },
    "mayorista": {
        "Serie": "272",
        "Detalle": "Tipo de Cambio Mayorista ($ por US$) Comunicación A 3500 - Referencia",
    },
    "TEAPF": {
        "Serie": "7939",
        "Detalle": "Tasa mínima para plazos fijos de personas humanas hasta $10 millones (en  e.a. para depósitos a 30 días)",
    },
    "inflacion": {"Serie": "7931", "Detalle": "Inflación mensual (variación en )"},
    "inflacionIA": {
        "Serie": "7932",
        "Detalle": "Inflación interanual (variación en i.a.)",
    },
    "reservas": {
        "Serie": "246",
        "Detalle": "Reservas Internacionales del BCRA (en millones de dólares - cifras provisorias sujetas a cambio de valuación)",
    },
    "inflacion": {"Serie": "7931",
                  "Detalle":"Inflación mensual (variación en )"},
    "leliq":{"Serie": "7926",
             "Detalle": "LELIQ saldos (en millones de pesos)"}

}

def variables_bcra(tipo="cer", desde="2016-04-01", hasta=None):

    variables = list(settings.keys())
    variables.remove("reservas")
    variables.remove("leliq")

    url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp"

    if not hasta:
        hasta = datetime.now().date().strftime("%Y-%m-%d")

    data = {
        "primeravez": "1",
        "fecha_desde": desde,
        "fecha_hasta": hasta,
        "serie": settings[tipo]["Serie"],
        "series1": "0",
        "series2": "0",
        "series3": "0",
        "series4": "0",
        "detalle": settings[tipo]["Detalle"],
    }
    resp = requests.post(url=url, data=data, headers={"User-Agent": "Mozilla/5.0"})

    r_text = resp.text

    df_cer = pd.read_html(r_text, thousands=".")[0]

    if tipo in variables:
        df_cer = df_cer.apply(lambda x: x.str.replace(",", "."))

    df_cer["Fecha"] = pd.to_datetime(df_cer["Fecha"], format="%d/%m/%Y").dt.date
    df_cer[["Valor"]] = df_cer[["Valor"]].astype("float64")
    df_cer.set_index("Fecha", inplace=True)
    df_cer.rename(columns={"Valor": tipo}, inplace=True)

    return df_cer


def dolar_mep(desde="2015-01-01", hasta=None):

    if not hasta:
        hasta = datetime.now().date().strftime("%Y-%m-%d")
        print(hasta)

    # MEP ordenado de mayor a menor comienza 24 03 2020
    url = f"https://mercados.ambito.com/dolarrava/mep/historico-general/{desde}/{hasta}"
    df_dolar = pd.read_json(url)
    df_dolar = df_dolar.reindex(index=df_dolar.index[::-1]).reset_index()
    df_dolar = df_dolar.drop(columns=["index"])
    df_dolar = df_dolar.apply(lambda x: x.str.replace(",", "."))
    df_dolar = df_dolar[:-1]
    df_dolar[[1]] = df_dolar[[1]].astype("float64")


    df_dolar = df_dolar[:-1]

    df_dolar = df_dolar.rename(columns={0: "Fecha", 1: "mep"})
    df_dolar["Fecha"] = pd.to_datetime(df_dolar["Fecha"], format="%d/%m/%Y").dt.date
    df_dolar.set_index("Fecha", inplace=True)

    return df_dolar


def dolar_ccl(start="2015-01-01"):
    tickers = ["GGAL", "GGAL.BA", "AAPL.BA", "AAPL", "ARS=X", "YPF", "YPFD.BA", "M.BA", "PAM", "PAMP.BA"]
    df_close = yf.download(tickers, start=start, auto_adjust=True)["Close"]
    df_close.dropna(inplace=True)
    df_close["cclgal"] = 10 * df_close["GGAL.BA"] / df_close["GGAL"]
    df_close["cclaapl"] = 10 * df_close["AAPL.BA"] / df_close["AAPL"]
    df_close["cclypf"] = df_close["YPFD.BA"] / df_close["YPF"]
    df_close["ccl"] = (df_close.cclgal + df_close.cclaapl + df_close.cclypf) / 3
    df_close["cclars"] = df_close.ccl / df_close["ARS=X"] - 1

    df_close["MervARS=X"] = df_close["M.BA"] / df_close["ARS=X"]

    return df_close

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

    exit()

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

