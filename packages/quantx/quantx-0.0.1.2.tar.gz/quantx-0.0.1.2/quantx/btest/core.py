from quantx.btest.data import Data
from quantx.btest.portfolio import Portfolio
from quantx.btest.scheduler import Scheduler
from quantx.factors.pipeline import Pipeline
from quantx.utils.const import OrderStat, Bar


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


class ExchContext:
    __instance__ = None
    _benchmark = None
    _short_allowed = False
    _portfolio = None
    _commission = None
    _data = None
    _scheduler = None

    _slippage = 0
    _capital = 0
    _lock_days = 0

    _open_orders = dict()
    _traded_dict = dict()
    _symbols = set()
    _total_orders = list()
    _total_trades = list()
    _pipeline = Pipeline()

    @property
    def pipeline(self) -> Pipeline:
        return self._pipeline

    @property
    def portfolio(self) -> Portfolio:
        return self._portfolio

    @property
    def cash(self):
        return self._capital

    @cash.setter
    def cash(self, value):
        self._capital = value

    @property
    def benchmark(self):
        return self._benchmark

    @benchmark.setter
    def benchmark(self, value):
        self._benchmark = value

    @property
    def short_allowed(self):
        return self._short_allowed

    @short_allowed.setter
    def short_allowed(self, value):
        self._short_allowed = value

    @property
    def slippage(self):
        return self._slippage

    @slippage.setter
    def slippage(self, value):
        self._slippage = value

    @property
    def lock_days(self):
        return self._lock_days

    @lock_days.setter
    def lock_days(self, value):
        self._lock_days = value

    @property
    def commission(self):
        return self._commission

    @commission.setter
    def commission(self, value):
        self._commission = value

    @property
    def traded_dict(self) -> dict:
        return self._traded_dict

    @property
    def symbols(self):
        return self._symbols

    @symbols.setter
    def symbols(self, value):
        self._symbols = value

    @property
    def scheduler(self) -> Scheduler:
        return self._scheduler

    @property
    def data(self) -> Data:
        return self._data

    def get_open_orders(self, symbol=None):
        return self._open_orders[symbol] if symbol else self._open_orders

    def get_order(self, order):
        return self._total_orders[order.id]

    def open_order(self, order):
        raise NotImplementedError

    def close_order(self, order):
        raise NotImplementedError

    def get_commission(self, order, amount=None):
        raise NotImplementedError

    def run(self,
            handle_bar,
            start_date=None,
            end_date=None,
            initialize=None,
            before_trading_start=None,
            after_trading_end=None):
        raise NotImplementedError


class Exch(ExchContext):
    def __init__(self):
        Exch.__instance__ = self

    @classmethod
    def get_context(cls) -> ExchContext:
        return cls.__instance__


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

    def _open(self, amount):
        self.status = OrderStat.OPEN
        self.amount = amount
        return Exch.get_context().open_order(self)

    def shares(self, symbol, amount):
        self.symbol = symbol

        lot = Exch.get_context().data.get_lot(symbol)
        amount = int(amount) // lot * lot if amount > 0 else int(amount)
        return self._open(amount)

    def lots(self, symbol, amount):
        return self.shares(symbol, amount * Exch.get_context().data.get_lot(symbol))

    def cash(self, symbol, cash):
        self.symbol = symbol

        price = self.price
        amount = cash / price
        cash -= Exch.get_context().get_commission(self, amount) if amount > 0 else 0
        return self.shares(symbol, cash / price)

    def portfolio_percent(self, symbol, percent):
        return self.cash(symbol, Exch.get_context().portfolio.value * percent)

    def target_market_value(self, symbol, market_value):
        return self.cash(symbol,
                         market_value - Exch.get_context().portfolio.get_position(symbol).market_value)

    def target_portfolio_percent(self, symbol, percent):
        return self.cash(symbol,
                         Exch.get_context().portfolio.value * percent -
                         Exch.get_context().portfolio.get_position(symbol).market_value)

    def target_position(self, symbol, amount):
        return self.shares(symbol, amount - Exch.get_context().portfolio.get_position(symbol).amount)

    @property
    def price(self):
        raise NotImplementedError

    def _close(self, stat):
        self.status = stat
        return Exch.get_context().close_order(self)

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


class QuoteDict:
    def __init__(self, bars):
        self.__bars = bars

    def __getitem__(self, symbol):
        return self.__bars[symbol][Bar.close]


class Txn:
    def handle(self, context, order):
        raise NotImplementedError
