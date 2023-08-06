from datetime import timedelta

from quantx.btest.core import Transaction, Order, ExchContext, Txn


class SimulationTxn(Txn):
    def cost_cal(self, context: ExchContext, order: Order, amount):
        return (order.price * amount) + context.get_commission(order, amount)

    def handle(self, context: ExchContext, order: Order):
        lock_dt = timedelta(days=context.lock_days)
        bar = context.data.get_bar(order.symbol)
        pos = context.portfolio.get_position(order.symbol)

        amount = order.amount - order.deal_amount
        deal_amount = amount if bar.vol >= amount else int(bar.vol) // bar.lot * bar.lot

        cost = self.cost_cal(context, order, deal_amount)  # commission_cal(pric * deal_amount)
        freezed = self.cost_cal(context, order, amount) - cost if order.amount > 0 else 0

        assert not context.data.is_stop(order.symbol), "[%s]已停牌,无法交易" % order.symbol
        assert bar.inc < bar.limit, \
            "[%s]已涨停,无法交易" % order.symbol
        assert bar.inc > -bar.limit, \
            "[%s]已跌停,无法交易" % order.symbol

        assert not deal_amount % bar.lot and abs(deal_amount) >= bar.lot or not order.amount > 0, \
            "买入数量[%d]必须为[%d]整数倍且至少买入一手" % (deal_amount, bar.lot)

        assert not context.portfolio.free < cost + freezed or not order.amount > 0, \
            "可用余额[%0.2f]少于[%0.2f]" % (context.portfolio.free, cost + freezed)

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
            price=order.price,
            amount=deal_amount,
            cost=cost,
            fee=context.get_commission(order, amount),
            freezed=freezed - order.freezed,
            unlock_dt=context.data.trading_day + lock_dt if lock_dt else None)
