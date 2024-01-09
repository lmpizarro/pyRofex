import pandas as pd
from datetime import datetime, timedelta
import requests

settings = {
    "cer": {"Serie": "3540", "Detalle": "CER (Base 2.2.2002=1)",
            "Serie1": "0",
            "Serie2": "0",
            },
    "badlar": {
        "Serie": "7935",
        "Detalle": "BADLAR en pesos de bancos privados (en  e.a.)",
        "Serie1": "0",
            "Serie2": "0",
    },
    "TEAPolMon": {
        "Serie": "7936",
        "Detalle": "Tasa de Política Monetaria (en  e.a.)",
        "Serie1": "0",
            "Serie2": "0",
    },
    "mayorista": {
        "Serie": "272",
        "Detalle": "Tipo de Cambio Mayorista ($ por US$) Comunicación A 3500 - Referencia",
        "Serie1": "0",
            "Serie2": "0",
    },
    "minorista": {
        "Serie": "7927",
        "Detalle": "Tipo de Cambio Minorista ($ por US$) Comunicación B 9791",
        "Serie1": "0",
            "Serie2": "0",
    },
    "TEAPF": {
        "Serie": "7939",
        "Detalle": "Tasa mínima para plazos fijos de personas humanas hasta $10 millones (en  e.a. para depósitos a 30 días)",
        "Serie1": "0",
            "Serie2": "0",
    },
    "inflacion": {"Serie": "7931",
                  "Detalle": "Inflación mensual (variación en )",
                  "Serie1": "0",
            "Serie2": "0",
                  },
    "inflacionIA": {
        "Serie": "7932",
        "Detalle": "Inflación interanual (variación en i.a.)",
        "Serie1": "0",
            "Serie2": "0",
    },
    "reservas": {
        "Serie": "246",
        "Detalle": "Reservas Internacionales del BCRA (en millones de dólares - cifras provisorias sujetas a cambio de valuación)",
        "Serie1": "0",
            "Serie2": "0",
    },
    "uva": {"Serie": "7913",
            "Detalle":"Unidad de Valor Adquisitivo (UVA) (en pesos -con dos decimales-, base 31.3.2016=14.05)",
            "Serie1": "0",
            "Serie2": "0",
            },
    "leliq":{"Serie": "7926",
             "Detalle": "LELIQ saldos (en millones de pesos)",
            "Serie1": "0",
            "Serie2": "0",
            },
    "circMonetaria": {"Serie": "251",
                      "Detalle": "Circulación monetaria (en millones de pesos)",
                      "Serie1": "0",
            "Serie2": "0",
                    },
    "depositoCtaCteBancos": {"Serie": "252",
                       "Detalle": "Depósitos de los bancos en cta. cte. en pesos en el BCRA (en millones de pesos)",
                       "Serie1": "0",
            "Serie2": "0",
                    },

    "fisicoPub": {"Serie": "251",
                  "Detalle": "Billetes y monedas en poder del público (en millones de pesos)",
                  "Serie1": "296",
            "Serie2": "0",
                },
    "depoEfecTotal": {"Serie": "444",
                  "Detalle": "Depósitos en efectivo en las entidades financieras - Total (en millones de pesos)",
                  "Serie1": "459",
            "Serie2": "3540",
                }
}

def variables_bcra(tipo="cer", desde="2016-04-01", hasta=None):

    variables = list(settings.keys())
    variables.remove("reservas")
    variables.remove("leliq")
    variables.remove("circMonetaria")
    variables.remove("depositoCtaCteBancos")
    variables.remove("fisicoPub")
    variables.remove("depoEfecTotal")


    url = "https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables_datos.asp"

    if not hasta:
        hasta = datetime.now().date().strftime("%Y-%m-%d")

    data = {
        "primeravez": "1",
        "fecha_desde": desde,
        "fecha_hasta": hasta,
        "serie": settings[tipo]["Serie"],
        "serie1": settings[tipo]["Serie1"],
        "serie2": settings[tipo]["Serie2"],
        "serie3": "0",
        "serie4": "0",
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

if __name__ == "__main__":
    df_cer = variables_bcra()
    df_infla = variables_bcra(tipo='inflacion', desde='2010-06-30')
    df_minorista = variables_bcra(tipo="minorista", desde='2010-01-31')
    new_row ={"inflacion": 12.4}
    new_df = pd.DataFrame.from_records([new_row], index=[datetime.now().date()])
    df_infla = pd.concat([df_infla, new_df])
    new_df = pd.DataFrame.from_records([{"inflacion": 0.0}], index=[df_infla.index[0]- timedelta(days=30)])
    df_infla = pd.concat([new_df, df_infla])
    # df_infla = pd.merge(df_infla, df_minorista, left_index=True, right_index=True)

    df_infla['inflacion'] = 1 + df_infla['inflacion'] / 100
    df_infla['acumulada'] = df_infla['inflacion'].cumprod()
    print(df_infla.head())


    print(df_infla.tail())
    print()


    print(df_minorista.iloc[-1].minorista/df_minorista.iloc[0].minorista)

    print(df_minorista.tail())

    df_cirMon = variables_bcra(tipo='circMonetaria', desde='2010-06-30')
    dfMerge =  pd.merge(df_cirMon, df_minorista, left_index=True, right_index=True)

    print(df_cirMon.tail())

    df_depo = variables_bcra(tipo='depositoCtaCteBancos', desde='2010-06-30')
    dfMerge =  pd.merge(df_depo, dfMerge, left_index=True, right_index=True)

    print(df_depo.tail())

    df_depo = variables_bcra(tipo='fisicoPub', desde='2010-06-30')
    df_depoEfec = variables_bcra(tipo='depoEfecTotal', desde='2010-06-30')
    dfMerge =  pd.merge(df_depoEfec, dfMerge, left_index=True, right_index=True)

    print(df_depo.tail())
    dfMerge['circUSD'] = dfMerge['circMonetaria'] / dfMerge['minorista']
    dfMerge['depoCtaCteUSD'] = dfMerge['depositoCtaCteBancos'] / dfMerge['minorista']
    dfMerge['depoEfectUSD'] = dfMerge['depoEfecTotal'] / dfMerge['minorista']
    print(dfMerge.tail())

    import matplotlib.pyplot as plt

    plt.plot(dfMerge['circUSD'])
    plt.show()

    plt.plot(dfMerge['depoCtaCteUSD'])
    plt.show()

    plt.plot(dfMerge['depoEfectUSD'])
    plt.show()

