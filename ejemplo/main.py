from datetime import datetime
from instruments import Ticker, ticker_to_operate, ticker_entries
from enums import ContractType, OrderType, Side
from order import Order, CreateOrder
from config import Config
import pyRofex
from decouple import config


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

    market_data = pyRofex.get_market_data(
        ticker=ticker_to_operate.name, entries=ticker_entries, depth=2)

    print('Ticker ', ticker_to_operate.name)
    print("LAST  {0}: ".format(
        market_data['marketData']['LA']))
    print("BID {0}: ".format(market_data['marketData']['BI']))
    print("OFFER {0}: ".format(market_data['marketData']['OF']))


if __name__ == "__main__":
    main()
