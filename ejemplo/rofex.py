from datetime import datetime, timedelta
import pyRofex
from instruments import Ticker
from dataclasses import dataclass, field
from typing import Any
from periods import by_days
import pandas as pd
import numpy as np
from order import Order
from enums import OrderType


dlr_ene_24 = Ticker(name='DLR/ENE24', cash_asigned=10_000)
ggal_ago_23 = Ticker(name='GGAL/AGO23', cash_asigned=10_000)

ticker_entries = [pyRofex.MarketDataEntry.BIDS,
                  pyRofex.MarketDataEntry.OFFERS, pyRofex.MarketDataEntry.LAST]


@dataclass(frozen=True)
class Rofex:
    tickers: list[Ticker] = field(default=list)
    entries: list[pyRofex.MarketDataEntry] = field(default=list)

    def fetch_market_data(self, depth=2) -> list[Any]:
        market_data = {}

        for ticker in self.tickers:

            md = pyRofex.get_market_data(
                ticker=ticker.name, entries=self.entries, depth=depth)
            if md['status'] == 'OK':
                market_data[ticker] = md['marketData']

        return market_data

    def fetch_history(self, days=5):
        history = {}
        end, start = by_days(days=days)

        for ticker in self.tickers:
            historic_trades = pyRofex.get_trade_history(
                ticker=ticker.name, start_date=start, end_date=end)
            if historic_trades['status'] == 'OK':
                history[ticker] = historic_trades['trades']
        return history

    @staticmethod
    def hist_agg(history:dict, ticker: Ticker) -> pd.DataFrame:
        df = pd.DataFrame.from_records(history[ggal_ago_23])

        df['date'] = pd.to_datetime(df['datetime']).dt.date
        gr = df.groupby(['date'])
        result = gr.agg(Low=('price', np.min), High=('price', np.max),
                        Mean=('price', np.mean), Vol=('size', np.sum))
        result['Open'] = gr.price.first()
        result['Close'] = gr.price.last()
        return result

    @staticmethod
    def buy(order: Order):
        order_type = pyRofex.OrderType.LIMIT
        if order.limit == OrderType.MARKET:
            order_type = pyRofex.OrderType.MARKET

        order = pyRofex.send_order(ticker=order.ticker.name,
                                    side=pyRofex.Side.BUY,
                                    size=order.size,
                                    price=order.price,
                                    order_type=order_type)
        return order


    @staticmethod
    def sell(order: Order):
        ...

    @staticmethod
    def cancel(id:str):
        return pyRofex.cancel_order(id)

    @staticmethod
    def status(id:str):
        """
        NEW
        PENDING_NEW
        PENDING_REPLACE
        PENDING_CANCEL
        REJECTED
        PENDING_APPROVAL
        CANCELLED
        REPLACED
        """
        status = pyRofex.get_order_status(id)
        print(status)

        if status['status'] == 'OK':
            return status['order']['status']




