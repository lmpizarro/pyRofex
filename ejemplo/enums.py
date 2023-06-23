from enum import Enum

class ContractType(str, Enum):
    OPTION = 'OPTION'
    STOCK = 'STOCK'
    FUTURE = 'FUTURE'


class Side(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'


class OrderType(str, Enum):
    LIMIT = 'LIMIT'
    MARKET = 'MARKET'

