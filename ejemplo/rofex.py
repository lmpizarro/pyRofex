import pandas as pd
import numpy as np
from typing import Any
from dataclasses import dataclass, field
import pyRofex
from instruments import TickerList
from periods import by_days
from order import Order
from enums import OrderType
from order_book import OrderBook, OrderBookContainer, OrderBookItem, Last


@dataclass(frozen=True)
class MarketData:
    tickers: list[TickerList] = field(default=list)
    entries: list[pyRofex.MarketDataEntry] = field(default=list)
    account: str = field(default='')
    environment: str = field(default='')

    @staticmethod
    def create_order_book(md_rofex: dict[Any, Any]) -> OrderBook:
        bids = md_rofex['marketData']['OF']
        asks = md_rofex['marketData']['BI']
        list_bids = [OrderBookItem(price=e['price'], size=e['size']) for e in bids]
        list_asks = [OrderBookItem(price=e['price'], size=e['size']) for e in asks]
        last_price = md_rofex['marketData']['LA']
        return OrderBook(list_bids, list_asks, Last(**last_price))


    def fetch_market_data(self, container: OrderBookContainer, depth=2) -> None:

        """Fetch market data for instruments"""

        for ticker in self.tickers:

            md = pyRofex.get_market_data(
                ticker=ticker.name, entries=self.entries, depth=depth)
            if md['status'] == 'OK':
                container.add(ticker, MarketData.create_order_book(md_rofex=md))

    def fetch_history(self, days=5):
        """Fetch history for instruments from Rofex"""
        history = {}
        end, start = by_days(days=days)

        for ticker in self.tickers:
            historic_trades = pyRofex.get_trade_history(
                ticker=ticker.name, start_date=start, end_date=end)
            if historic_trades['status'] == 'OK':
                history[ticker] = historic_trades['trades']
        return history

    def positions(self):
        """Get positions from rofex account"""
        return pyRofex.get_account_position(account=self.account, environment=self.environment)

    @staticmethod
    def hist_agg(history: list) -> pd.DataFrame:
        """Aggregate history to obtain HLCO candles by day"""
        df = pd.DataFrame.from_records(history)

        df['date'] = pd.to_datetime(df['datetime']).dt.date
        gr = df.groupby(['date'])
        result = gr.agg(Low=('price', np.min), High=('price', np.max),
                        Mean=('price', np.mean), Vol=('size', np.sum))
        result['Open'] = gr.price.first()
        result['Close'] = gr.price.last()
        return result


class Operations:

    @staticmethod
    def buy(order: Order):
        """Execute buy order"""
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
        """Execute sell order"""
        order_type = pyRofex.OrderType.LIMIT
        if order.limit == OrderType.MARKET:
            order_type = pyRofex.OrderType.MARKET

        order = pyRofex.send_order(ticker=order.ticker.name,
                                   side=pyRofex.Side.SELL,
                                   size=order.size,
                                   price=order.price,
                                   order_type=order_type)
        return order

    @staticmethod
    def cancel(id: str):
        """Cancel Order"""
        return pyRofex.cancel_order(id)

    @staticmethod
    def status(id: str):
        """
        Get the status of a rofex order

        NEW, PENDING_NEW, PENDING_REPLACE, PENDING_CANCEL, REJECTED,
        PENDING_APPROVAL, CANCELLED, REPLACED

        https://www.onixs.biz/fix-dictionary/4.4/msgtype_8_8.html
        """
        status = pyRofex.get_order_status(id)
        print(status)

        if status['status'] == 'OK':
            return status['order']['status']
        else:
            return status['status']
