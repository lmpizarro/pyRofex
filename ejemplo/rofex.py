import pyRofex
from instruments import Ticker
from dataclasses import dataclass, field
from typing import Any


dlr_ene_24 = Ticker(name='DLR/ENE24', cash_asigned=10_000)
ggal_ago_23 = Ticker(name='GGAL/AGO23', cash_asigned=10_000)

ticker_to_operate = ggal_ago_23
ticker_entries = [pyRofex.MarketDataEntry.BIDS,
                  pyRofex.MarketDataEntry.OFFERS, pyRofex.MarketDataEntry.LAST]


@dataclass(frozen=True)
class Rofex:
    tickers: list[Ticker] = field(default=list)
    entries: list[pyRofex.MarketDataEntry] = field(default=list)

    def market_data(self, depth=2)->list[Any]:
        market_data = []

        for ticker in self.tickers:

           md = pyRofex.get_market_data(
            ticker=ticker.name, entries=self.entries, depth=depth)
           if md['status'] == 'OK':
                market_data.append(md['marketData'])

        return market_data





