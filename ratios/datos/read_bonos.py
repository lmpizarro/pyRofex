import pandas as pd

def read_bono(filename):


    df_bono = pd.read_csv(filename)

    df_bono["Fecha"] = pd.to_datetime(df_bono["fecha"], format="%Y-%m-%d").dt.date
    df_bono.set_index("Fecha", inplace=True)
    df_bono.drop(['fecha'], axis=1)

    return df_bono


def read_bonos_dolar():
    years =[29, 30, 35, 38, 41]
    format_filename = "{0}D - Cotizaciones historicas.csv"
    for year in years:

        key_gd = f"gd{year}".upper()
        key_al = (f"al{year}" if year != 38 else f"ae{year}").upper()

        filename_gd = format_filename.format(key_gd)
        filename_al = format_filename.format(key_al)

        print(filename_gd, filename_al)

        df_gd = read_bono(filename=filename_gd)
        df_al = read_bono(filename=filename_al)

        print(df_al.tail())


        import matplotlib.pyplot as plt

        plt.plot(df_al.cierre)
        plt.show()


if __name__ == "__main__":
    read_bonos_dolar()
