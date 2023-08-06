import abc
import math


class Slippage:
    @abc.abstractclassmethod
    def handle(self, bar, order):
        pass


class VolumeShareSlippage(Slippage):
    def __init__(self, volume_rate=0.25, price_rate=0.0):
        self.vol_rate = volume_rate
        self.price_rate = price_rate

    def handle(self, bar, order):
        amount = order.amount - order.deal_amount
        vol = min(bar.vol * self.vol_rate, abs(amount))
        impact_rate = min(vol / bar.vol, self.vol_rate)
        impact_price = impact_rate ** 2 * math.copysign(self.price_rate * order.price, order.direction)
        return order.price + impact_price


class FixedSlippage(Slippage):
    def __init__(self, price_rate=0.0):
        self.price_rate = price_rate

    def handle(self, bar, order):
        return order.price + ((order.price * self.price_rate) / 2 * order.direction)
