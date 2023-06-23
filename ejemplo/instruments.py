from dataclasses import dataclass
import pyRofex


@dataclass
class Ticker:
    name: str
    cash_asigned: float


dlr_ene_24 = Ticker(name='DLR/ENE24', cash_asigned=10_000)
ggal_ago_23 = Ticker(name='GGAL/AGO23', cash_asigned=10_000)

ticker_to_operate = ggal_ago_23
ticker_entries = [pyRofex.MarketDataEntry.BIDS,
                  pyRofex.MarketDataEntry.OFFERS, pyRofex.MarketDataEntry.LAST]
