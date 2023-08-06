from quantx.btest.core import Order, Exch
from quantx.utils.const import Bar


class MarketOrder(Order):
    @property
    def price(self):
        return Exch.get_context().data.get_quote(self.symbol)


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
