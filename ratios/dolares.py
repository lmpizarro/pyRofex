from datetime import datetime
import pandas as pd
import yfinance as yf

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

