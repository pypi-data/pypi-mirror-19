from quantx.btest.core import Order, Exch



class MarketOrder(Order):
    @property
    def price(self):
        return Exch.get_context().data.last("close",self.symbol)


class LimitOrder(Order):
    def __init__(self, limit):
        self.limit = limit

    @property
    def price(self):
        return self.limit


class StopOrder(Order):
    def __init__(self, stop):
        self.stop = stop


class StopLimitOrder(Order):
    def __init__(self, limit, stop):
        self.limit = limit
        self.stop = stop
