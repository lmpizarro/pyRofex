from datetime import datetime
from decouple import config
import pyRofex
from instruments import Ticker
from rofex import ticker_entries, MarketData, ggal_ago_23
from rofex import Operations as rfx_operations
from enums import ContractType, OrderType, Side
from order import Order, CreateOrder
from config import Config


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


def now_time() -> str:
    return str(datetime.now(
        tz=local_config.project_tz).isoformat()).split('.')[0]


def main():
    rfx_md = MarketData(tickers=[ggal_ago_23], entries=ticker_entries, account=config(
        'ACCOUNT'), environment=pyRofex.Environment.REMARKET)
    market_data = rfx_md.fetch_market_data()
    print(market_data[ggal_ago_23])
    print(market_data[ggal_ago_23].spread())


    history = rfx_md.fetch_history(days=40)
    aggregate = rfx_md.hist_agg(history=history, ticker=ggal_ago_23)
    print(aggregate)

    my_order = CreateOrder.buy_stock_limit(
        symbol=ggal_ago_23, units=10, price=800, date_time=now_time())

    # order_status = rfx.buy(order=my_order)

    # print(order_status)
    print('...', rfx_operations.status('426356796424478'))

    print(rfx_md.positions())


if __name__ == "__main__":
    main()
