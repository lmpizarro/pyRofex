from datetime import datetime
from functools import partial
from decouple import config
import pyRofex
from instruments import Ticker
from rofex import ticker_entries, Rofex, dlr_ene_24, ggal_ago_23
from enums import ContractType, OrderType, Side
from order import Order, CreateOrder
from config import Config
import pandas as pd


# 1-Initialize the environment
pyRofex.initialize(user=config('NAME'),
                   password=config('PASS'),
                   account=config('ACCOUNT'),
                   environment=pyRofex.Environment.REMARKET)


local_config = Config()


def test():
    ticker = Ticker(name="AAPL", cash_asigned=10_000)
    order = Order(ticker=ticker, contract=ContractType.STOCK,
                  side=Side.BUY, limit=OrderType.MARKET, size=10)

    print(order)
    iso_datetime = str(datetime.now(
        tz=local_config.project_tz).isoformat()).split('.')[0]
    ticker = Ticker(name='TSLA', cash_asigned=10_0000)
    CreateOrder.buy_stock_limit(
        symbol=ticker, units=10, price=100, date_time=iso_datetime)
    CreateOrder.sell_stock_limit(
        symbol=ticker, units=10, price=100, date_time=iso_datetime)
    CreateOrder.buy_stock_market(
        symbol=ticker, units=10, date_time=iso_datetime)
    order = CreateOrder.sell_stock_market(
        symbol=ticker, units=10, date_time=iso_datetime)

    print(order)

    print(order.json)


def main():
    rfx = Rofex(tickers=[ggal_ago_23], entries=ticker_entries)
    market_data = rfx.fetch_market_data()
    print(market_data)

    history = rfx.fetch_history(days=40)
    aggregate = rfx.hist_agg(history=history, ticker=ggal_ago_23)
    print(aggregate)

if __name__ == "__main__":
    main()
