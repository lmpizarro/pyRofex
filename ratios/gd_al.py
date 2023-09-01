from rava import scrap_bonos_rava, coti_hist
import pandas as pd
import matplotlib.pyplot as plt


def ratio_bond_usd(year: str = 29):
    key_gd = f"gd{year}"
    hist_gd = coti_hist(scrap_bonos_rava(key_gd))
    key_bond = f"al{year}" if year != 38 else f"ae{year}"
    hist_al = coti_hist(scrap_bonos_rava(key_bond))

    cierre_gd = hist_gd[["fecha", "cierre", "usd_cierre"]]
    cierre_al = hist_al[["fecha", "cierre", "usd_cierre"]]
    mrg = pd.merge(
        cierre_al, cierre_gd, on="fecha", suffixes=(f"_al{year}", f"_gd{year}")
    )
    mrg[f"usd_al{year}"] = mrg[f"cierre_al{year}"] / mrg[f"usd_cierre_al{year}"]
    mrg[f"usd_gd{year}"] = mrg[f"cierre_gd{year}"] / mrg[f"usd_cierre_gd{year}"]
    mrg[f"ratio_{year}"] = mrg[f"cierre_gd{year}"] / mrg[f"cierre_al{year}"]
    mrg[f"ratio_usd_{year}"] = mrg[f"usd_cierre_gd{year}"] / mrg[f"usd_cierre_al{year}"]

    mrg["fecha"] = pd.to_datetime(mrg["fecha"], format="%Y-%m-%d").dt.date
    mrg.set_index("fecha", inplace=True)

    plt.plot(mrg[f"ratio_usd_{year}"])
    plt.title(f"{key_gd}/{key_bond}")
    plt.show()


def ratios_bonos_dolar():
    years =[29, 30, 35, 38, 41]
    for y in years:
        ratio_bond_usd(y)


if __name__ == "__main__":
    ratios_bonos_dolar()
