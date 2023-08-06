import abc
from quantx.btest.benchmark import Benchmark
from quantx.btest.commission import Commission
from quantx.btest.data import Data
from quantx.btest.portfolio import Portfolio
from quantx.btest.scheduler import Scheduler
from quantx.btest.slippage import Slippage

from quantx.factors.pipeline import Pipeline


class Exch:
    _benchmark = None
    _short_allowed = False
    _portfolio = None
    _commission = None
    _data = None
    _scheduler = None

    _slippage = 0
    _starting_cash = 0
    _lock_days = 0

    _open_orders = dict()
    _traded_dict = dict()
    _symbols = set()
    _records = dict()
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
    def starting_cash(self):
        return self._starting_cash

    @starting_cash.setter
    def starting_cash(self, value):
        self._starting_cash = value

    @property
    def benchmark(self) -> Benchmark:
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
    def slippage(self) -> Slippage:
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
    def commission(self) -> Commission:
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

    def __init__(self):
        from quantx.btest.ctx import ExchContext
        ExchContext.__instance__ = self

    def get_open_orders(self, symbol=None):
        return self._open_orders[symbol] if symbol else self._open_orders

    def get_order(self, order_id):
        if isinstance(order_id, int):
            return self._total_orders[order_id]
        else:
            return self._total_orders[order_id.id]

    @abc.abstractclassmethod
    def open_order(self, order):
        pass

    @abc.abstractclassmethod
    def close_order(self, order):
        pass

    def record(self, **kwargs):
        for key, value in kwargs.items():
            self._records.setdefault(key, [None] * self.data.trading_day_ix)
            rlen = self.data.trading_day_ix - len(self._records[key])
            self._records[key] += [None] * rlen + [value]

    @abc.abstractclassmethod
    def run(
            self,
            handle_bar,
            start_date=None,
            end_date=None,
            initialize=None,
            analyze=None,
            out_path=None
    ):
        pass
