from quantx.utils.const import OrderStat
from quantx.btest.ctx import ExchContext


class Order:
    id = None
    limit = 0
    stop = 0
    amount = 0
    symbol = None
    status = None
    avg_pric = 0
    deal_cost = 0
    deal_amount = 0
    freezed = 0
    create_date = None
    finish_date = None
    error = None

    def __eq__(self, other):
        return self.id == other.id

    @property
    def direction(self):
        return 1 if self.amount > 0 else -1

    def _open(self, amount):
        self.status = OrderStat.OPEN
        self.amount = amount
        return ExchContext.get_exch().open_order(self)

    def shares(self, symbol, amount):
        self.symbol = symbol

        lot = ExchContext.get_exch().data.last("lot", symbol)
        amount = int(amount) // lot * lot if amount > 0 else int(amount)
        return self._open(amount)

    def lots(self, symbol, amount):
        return self.shares(symbol, amount * ExchContext.get_exch().data.last("lot", symbol))

    def cash(self, symbol, cash):
        self.symbol = symbol

        price = self.price
        amount = cash / price
        cash -= ExchContext.get_exch().commission.handle(symbol, price, amount) if amount > 0 else 0
        return self.shares(symbol, cash / price)

    def portfolio_percent(self, symbol, percent):
        return self.cash(symbol, ExchContext.get_exch().portfolio.value * percent)

    def target_market_value(self, symbol, market_value):
        return self.cash(symbol,
                         market_value - ExchContext.get_exch().portfolio.get_position(symbol).market_value)

    def target_portfolio_percent(self, symbol, percent):
        return self.cash(symbol,
                         ExchContext.get_exch().portfolio.value * percent -
                         ExchContext.get_exch().portfolio.get_position(symbol).market_value)

    def target_position(self, symbol, amount):
        return self.shares(symbol, amount - ExchContext.get_exch().portfolio.get_position(symbol).amount)

    @property
    def price(self):
        raise NotImplementedError

    def _close(self, stat):
        self.status = stat
        return ExchContext.get_exch().close_order(self)

    def cancel(self):
        return self._close(OrderStat.CANCEL)

    def finish(self):
        return self._close(OrderStat.FINISH)

    def part(self):
        self.status = OrderStat.PART
        return

    def rejected(self, error):
        self.error = error
        return self._close(OrderStat.REJECTED)


class MarketOrder(Order):
    @property
    def price(self):
        return ExchContext.get_exch().data.last("close", self.symbol)


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
