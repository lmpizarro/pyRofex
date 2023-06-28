from instruments import Ticker
from dataclasses import dataclass


@dataclass
class OrderBookItem:
    price: float
    size: float

@dataclass
class Last:
    price: float
    size: float
    date: int


@dataclass
class Spread:
    bid: OrderBookItem
    offer: OrderBookItem
    spread: float
    spread_pc: float
    last: Last


class OrderBook:
    def __init__(self, _offer: list[OrderBookItem], _bid: list[OrderBookItem], _la: float) -> None:
        self.offer: list(OrderBookItem) = _offer
        self.bid: list(OrderBookItem) = _bid
        self.la: float = _la

    def __str__(self) -> str:
        return f'LA {self.la} BI {self.bid} OF {self.offer} '

    @staticmethod
    def weighted_mean(list_order_book_item: list[OrderBookItem]) -> float:
        w_mean = 0
        return w_mean

    def spread(self):
        of_mean = OrderBook.weighted_mean(self.offer)
        bi_mean = OrderBook.weighted_mean(self.bid)

        if not self.bid or not self.offer:
            return 0, 0, 0, 0

        if len(self.bid) != 0 and len(self.offer) != 0:
            spread = self.offer[0].price - self.bid[0].price
            spread_pc = spread / \
                (self.offer[0].price + self.bid[0].price)
            all_spread = Spread(bid=self.bid[0], offer=self.offer[0], spread=spread, spread_pc=spread_pc, last=self.la)
            return all_spread
        elif len(self.bid) != 0:
            return - self.bid[0].price, -1, self.bid[0].price, 0
        elif len(self.offer) != 0:
            return self.offer[0].price, 1, 0, self.offer[0].price

    def bid_ask(self):

        if len(self.bid) != 0 and len(self.offer) != 0:
            return (self.bid[0].price, self.offer[0].price)
        return (0, 0)


class OrderBookContainer:
    """ A container for Order Books"""

    def __init__(self) -> None:
        self.order_books: dict[Ticker, OrderBook] = {}

    def add(self, ticker: Ticker, order_book: OrderBook):
        """ add and order book for a ticker"""
        self.order_books[ticker] = order_book

    def get(self, ticker: Ticker) -> OrderBook:
        """ return the order book for a ticker"""
        return self.order_books[ticker]

    def keys(self):
        return self.order_books.keys()

    def list(self) -> list[tuple[Ticker, OrderBook]]:
        """return a list of pairs ticker order_book"""
        return list(self.order_books.items())
