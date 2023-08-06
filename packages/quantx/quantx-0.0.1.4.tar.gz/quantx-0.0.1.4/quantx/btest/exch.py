from pandas import DataFrame
from tqdm import tqdm

from quantx.btest.benchmark import Benchmark
from quantx.btest.commission import AStockCommission
from quantx.btest.core import Exch, Order
from quantx.btest.data import Data
from quantx.btest.portfolio import Portfolio
from quantx.btest.risk import Risk
from quantx.btest.scheduler import Scheduler, time_rule, date_rule
from quantx.btest.txn import SimTxn
from quantx.btest.until import log
from quantx.utils.const import DateFormat, Bar


class SimulationExch(Exch):
    _benchmark = "000001"
    _capital = 1000000
    _commission = AStockCommission()
    _risk = None
    _tqdm = None

    def __init__(self):
        Exch.__init__(self)

        self._txn = SimTxn()

    def __del__(self):
        if self._tqdm:
            self._tqdm.close()
        self._tqdm = None

    def open_order(self, order: Order):
        assert order.symbol in self._data.symbols

        order.id = self._total_orders.__len__()
        order.create_date = self._data.trading_day

        self._open_orders.setdefault(order.symbol, [])
        self._open_orders[order.symbol].append(order)
        self._total_orders.append(order)

        return order.id

    def close_order(self, order: Order):
        order.finish_date = self._data.trading_day

        self._open_orders[order.symbol].remove(order)

        if not self._open_orders[order.symbol]:
            self._open_orders.pop(order.symbol)

        self._traded_dict.setdefault(order.symbol, 0)
        self._traded_dict[order.symbol] += 1
        return order.id

    def get_commission(self, order: Order, amount=None):
        return self._commission.get(order, amount)

    def handle_order(self, order):
        try:
            txn = self._txn.handle(self, order)

            order.deal_amount += txn.amount
            order.deal_cost += txn.cost
            order.freezed = txn.freezed
            order.avg_price = abs(order.deal_cost / order.deal_amount)

            if order.amount - order.deal_amount:
                order.part()
            else:
                order.finish()

            log("[%s] %s SYMBOL:%s PRICE:%0.2f AMOUNT:%d %s , COST:%0.2f FEE:%0.2f FREEZED:%0.2f" % (
                txn.date.strftime(DateFormat.day),
                "BUY" if order.amount > 0 else "SELL",
                order.symbol,
                txn.price,
                txn.amount,
                order.status.upper(),
                txn.cost,
                txn.fee,
                txn.freezed
            ))
            self._total_trades.append(txn)
            return txn
        except AssertionError as e:
            order.rejected(e)

            log("[%s] %s SYMBOL:%s amount:%f %s , %s" % (
                order.create_date.strftime(DateFormat.day),
                "BUY" if order.amount > 0 else "SELL",
                order.symbol,
                order.amount - order.deal_amount,
                order.status.upper(),
                order.error
            ))

    def handle_bar(self, context):
        quote = self._data.last(Bar.close)
        self.portfolio.update(self._data.trading_day, quote)
        self._benchmark.update(self._data.trading_day, quote)
        self._risk.update(self.portfolio.returns, self._benchmark.returns)

        self._handle_bar(self, self._data)

        for symbol in list(self._open_orders.keys()):
            for order in self._open_orders[symbol]:
                trans = self.handle_order(order)
                if trans:
                    self.portfolio.update_transaction(trans)
                else:
                    self.portfolio.update_freezed(-order.freezed)

        self._data.next()

        self._tqdm.update(1)

    def run(
            self,
            handle_bar,
            start_date=None,
            end_date=None,
            initialize=None,
            before_trading_start=None,
            after_trading_end=None,
            out_path=None,
            debug=False,
    ):

        self._handle_bar = handle_bar
        self._debug = debug

        self._data = Data(self, start_date, end_date)

        self._scheduler = Scheduler(self._data.trading_day_lst)
        self._scheduler.add(before_trading_start, date_rule.day(), time_rule.before_trading)
        self._scheduler.add(self.handle_bar, date_rule.day(), time_rule.trading)
        self._scheduler.add(after_trading_end, date_rule.day(), time_rule.after_trading)

        if initialize:
            initialize(self)

        self._benchmark = Benchmark(self._benchmark, self._capital)
        self._portfolio = Portfolio(self._capital)
        self._risk = Risk()

        self._tqdm = tqdm(total=len(self._data.trading_day_lst), desc="backtesting")
        while not self._data.empty:
            for func in self._scheduler.get_funcs(self._data.trading_day):
                if func: func(self)

        result = DataFrame({
            "beta": self._risk.beta_lst,
            "alpha": self._risk.alpha_lst,
            "sharpe": self._risk.sharpe_lst,
            "sortino": self._risk.sortino_lst,
            "volatility": self._risk.volatility_lst,
            "max_drawdown": self._risk.max_drawdown_lst,
            "downside_risk": self._risk.downside_risk_lst,
            "tracking_error": self._risk.tracking_error_lst,
            "total_returns": self.portfolio.returns.total_lst,
            "information_rate": self._risk.information_rate_lst,
            "annualized_returns": self.portfolio.returns.annual_lst,
            "benchmark_total_returns": self._benchmark.returns.total_lst,
            "benchmark_annualized_returns": self.benchmark.returns.annual_lst
        }, index=self._data.trading_day_lst)

        if out_path:
            result.to_pickle(out_path)

        return result
