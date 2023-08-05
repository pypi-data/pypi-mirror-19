from datetime import timedelta

from quantx.btest.core import Transaction, Order, ExchContext, Txn


class SimTxn(Txn):
    def cost_cal(self, context: ExchContext, order: Order, amount):
        return (order.price * amount) + context.get_commission(order, amount)

    def handle(self, context: ExchContext, order: Order):
        lock_dt = timedelta(days=context.lock_days)
        vol = context.data.get_volume(order.symbol)
        lot = context.data.get_lot(order.symbol)
        quote = context.data.get_quote(order.symbol)
        pos = context.portfolio.get_position(order.symbol)

        amount = order.amount - order.deal_amount
        deal_amount = amount if vol >= amount else vol

        cost = self.cost_cal(context, order, deal_amount)  # commission_cal(pric * deal_amount)
        freezed = self.cost_cal(context, order, amount) - cost if order.amount > 0 else 0

        chg = (context.data.get_quote(order.symbol) -
               context.data.get_quote(order.symbol, -1)) / context.data.get_quote(order.symbol, -1)

        assert not context.data.is_stop(order.symbol), "[%s]已停牌,无法交易" % order.symbol
        assert chg < context.data.get_limit(order.symbol), "[%s]已涨停,无法交易" % order.symbol
        assert chg > -context.data.get_limit(order.symbol), "[%s]已跌停,无法交易" % order.symbol

        assert not deal_amount % lot and abs(deal_amount) >= lot or not order.amount > 0, \
            "买入数量[%d]必须为[%d]整数倍且至少买入一手" % (deal_amount, lot)

        assert not context.portfolio.free < cost + freezed or not order.amount > 0, \
            "可用余额[%0.2f]少于[%0.2f]" % (context.portfolio.free, cost + freezed)

        assert not context.short_allowed and not pos.sellable < abs(deal_amount) or order.amount > 0, \
            "可卖数量[%d]少于[%d]" % (pos.sellable, abs(deal_amount))

        assert not order.limit or order.amount > 0 and not order.limit < quote, \
            "限价买单[%d]无法在[%d]成交" % (order.limit, quote)

        assert not order.limit or order.amount < 0 and not order.limit > quote, \
            "限价卖单[%d]无法在[%d]成交" % (order.limit, quote)

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
