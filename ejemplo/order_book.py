class OrderBook:
    def __init__(self, _offer, _bid, _la, _depth) -> None:
        self.offer = _offer
        self.bid = _bid
        self.la = _la
        self.depth = _depth

    def __str__(self) -> str:
        return f'depth {self.depth} LA {self.la} BI {self.bid} OF {self.offer} '

    @staticmethod
    def weighted_mean(list_dict):
        w_mean = 0
        if list_dict and len(list_dict) != 0:
            w_mean = sum([of['price'] * of['size'] for of in list_dict]
                         ) / sum([of['size'] for of in list_dict])
        return w_mean

    def spread(self):
        of_mean = OrderBook.weighted_mean(self.offer)
        bi_mean = OrderBook.weighted_mean(self.bid)

        if not self.bid or not self.ask:
            return 0, 0, 0, 0

        if len(self.bid) != 0 and len(self.offer) != 0:
            spread = self.offer[0]['price'] - self.bid[0]['price']
            spread_pc = spread / \
                (self.offer[0]['price'] + self.bid[0]['price'])
            return spread, spread_pc, bi_mean, of_mean
        elif len(self.bid) != 0:
            return - self.bid[0]['price'], -1, bi_mean, of_mean
        elif len(self.offer) != 0:
            return self.offer[0]['price'], 1, bi_mean, of_mean

