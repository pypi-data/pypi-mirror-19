import abc
from datetime import timedelta

from quantx.btest.exch import Exch
from quantx.btest.order import Order
from pandas import isnull


class Txn:
    @abc.abstractclassmethod
    def handle(self, context, order):
        pass


class SimulationTxn(Txn):
    def cost_cal(self, context: Exch, symbol, price, amount):
        return (price * amount) + context.commission.handle(symbol, price, amount)

    def handle(self, context: Exch, order: Order):
        lock_dt = timedelta(days=context.lock_days)
        bar = context.data.get_bar(order.symbol)
        pos = context.portfolio.get_position(order.symbol)

        price = context.slippage.handle(bar, order)
        amount = order.amount - order.deal_amount

        deal_amount = amount if bar.vol >= amount else bar.vol

        cost = self.cost_cal(context, order.symbol, price, deal_amount)
        total_cost = self.cost_cal(context, order.symbol, price, amount)
        freezed = total_cost - cost if order.direction > 0 else 0

        assert bar.close, "[%s]已退市,无法交易" % order.symbol

        assert bar.active and bar.vol, "[%s]已停牌,无法交易" % order.symbol

        assert order.direction < 0 or bar.inc < bar.limit, \
            "[%s]已涨停,无法买入" % order.symbol

        assert order.direction > 0 or bar.inc > -bar.limit, \
            "[%s]已跌停,无法卖出" % order.symbol

        assert not deal_amount % bar.lot and abs(deal_amount) >= bar.lot or not order.amount > 0, \
            "买入数量[%d]必须为[%d]整数倍且至少买入一手" % (deal_amount, bar.lot)

        assert not context.portfolio.free < total_cost or not order.amount > 0, \
            "可用余额[%0.2f]少于[%0.2f]" % (context.portfolio.free, total_cost)

        assert not context.short_allowed and not pos.sellable < abs(deal_amount) or order.amount > 0, \
            "可卖数量[%d]少于[%d]" % (pos.sellable, abs(deal_amount))

        assert not order.limit or order.amount > 0 and not order.limit < bar.close, \
            "限价买单[%d]无法在[%d]成交" % (order.limit, bar.close)

        assert not order.limit or order.amount < 0 and not order.limit > bar.close, \
            "限价卖单[%d]无法在[%d]成交" % (order.limit, bar.close)

        return Transaction(
            symbol=order.symbol,
            date=context.data.trading_day,
            order_id=order.id,
            price=price,
            amount=deal_amount,
            cost=cost,
            fee=context.commission.handle(order.symbol, price, deal_amount),
            freezed=freezed - order.freezed,
            unlock_dt=context.data.trading_day + lock_dt if lock_dt else None)


class Transaction:
    symbol = None
    price = 0
    amount = 0
    cost = 0
    fee = 0
    freezed = 0
    unfreeze = 0
    unlock_dt = None
    date = None
    order_id = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
