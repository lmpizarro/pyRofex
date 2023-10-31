from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Ticker:
    name: str
    cash_asigned: float


class TickerList:
    def __init__(self, tickers: list[Ticker]):
        self.tickers: list[Ticker] = tickers

    def add(self, ticker: Ticker):
        self.tickers.append(ticker)

    def __iter__(self):
        return TickerListIterator(self)

    def to_list(self):
        return self.tickers


class TickerListIterator:
    def __init__(self, ticker_list: TickerList) -> None:
        self._ticker_list = ticker_list
        self._size = len(self._ticker_list.tickers)
        self._current_index = 0

    def __iter__(self):
        return self

    def __next__(self):

        if self._current_index < self._size:
            ticker = self._ticker_list.tickers[self._current_index]
            self._current_index += 1
            return ticker

        raise StopIteration


def main():
    rofex_ticker_list = [
        Ticker(name='DLR/NOV23', cash_asigned=10_000),
        Ticker(name='DLR/DIC23', cash_asigned=10_000),
        Ticker(name='DLR/ENE24', cash_asigned=10_000),
        Ticker(name='DLR/FEB24', cash_asigned=10_000),
        Ticker(name='DLR/MAR24', cash_asigned=10_000),
        Ticker(name='DLR/ABR24', cash_asigned=10_000),
                         ]

    tickers = TickerList(rofex_ticker_list)

    print(tickers.to_list())

    for t in tickers:
        print(t)



if __name__ == '__main__':
    main()
