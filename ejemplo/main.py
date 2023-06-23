from datetime import datetime
from instruments import Ticker, dlr_ene_24
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
    ticker =Ticker(name="AAPL", cash_asigned=10_000)
    order = Order(ticker=ticker, contract=ContractType.STOCK,
                  side=Side.BUY, limit=OrderType.MARKET, size=10)

    print(order)
    iso_datetime = str(datetime.now(tz=local_config.project_tz).isoformat()).split('.')[0]
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

    entries = [pyRofex.MarketDataEntry.BIDS, pyRofex.MarketDataEntry.OFFERS, pyRofex.MarketDataEntry.LAST]
    market_data = pyRofex.get_market_data(ticker=dlr_ene_24.name, entries=entries, depth=2)

    print("Market Data Response for {0}: {1}".format(dlr_ene_24.name, market_data['marketData']))




if __name__ == "__main__":
    main()

