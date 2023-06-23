from dataclasses import dataclass, field, asdict
from typing import Optional
from json import dumps
from enums import ContractType, Side, OrderType
from instruments import Ticker


@dataclass(frozen=True)
class Order:
    ticker: Ticker
    contract: ContractType
    side: Side
    limit: OrderType
    size: int = field(repr=False)
    price: int = field(default=None, repr=False)
    date_time: str = field(default=None, repr=True)

    def __post_init__(self):

        if not isinstance(self.ticker, Ticker):
            raise ValueError('must be ticker')

        if self.price and self.price < 0:
            raise ValueError('Price must be GT zero')

        if self.limit == OrderType.LIMIT and self.price == 0:
            raise ValueError(
                f'For {OrderType.LIMIT} order price must be not zero')

        if self.date_time and not isinstance(self.date_time, str):
            raise TypeError("date_time must be string")

        splited_date1 = self.date_time.split('-') if self.date_time else []
        splited_date2 = splited_date1[-1].split(
            ':') if len(splited_date1) != 0 else []
        if splited_date1 and (len(splited_date1) != 3 or len(splited_date2) != 3):
            raise TypeError("date_time bad formating")

    @property
    def __dict__(self):
        return asdict(self)

    @property
    def json(self):
        return dumps(self.__dict__)


class CreateOrder:
    @staticmethod
    def buy_stock_limit(symbol: Ticker, units: int, price: int,
                        date_time: Optional[str] = None) -> Order:
        return Order(ticker=symbol, contract=ContractType.STOCK, side=Side.BUY,
                     limit=OrderType.LIMIT, size=units, price=price, date_time=date_time)

    @staticmethod
    def sell_stock_limit(symbol: Ticker, units: int, price: int,
                         date_time: Optional[str] = None) -> Order:
        return Order(ticker=symbol, contract=ContractType.STOCK, side=Side.SELL,
                     limit=OrderType.LIMIT, size=units, price=price, date_time=date_time)

    @staticmethod
    def buy_stock_market(symbol: Ticker, units: int,
                         date_time: Optional[str] = None) -> Order:
        return Order(ticker=symbol, contract=ContractType.STOCK, side=Side.BUY,
                     limit=OrderType.MARKET, size=units, date_time=date_time)

    @staticmethod
    def sell_stock_market(symbol: Ticker, units: int,
                          date_time: Optional[str] = None) -> Order:
        return Order(ticker=symbol, contract=ContractType.STOCK, side=Side.SELL,
                     limit=OrderType.MARKET, size=units, date_time=date_time)


def main():
    ...


if __name__ == '__main__':
    main()
