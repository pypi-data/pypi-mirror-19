from pandas import DataFrame, concat
from tqdm import tqdm

from quantx.btest.benchmark import Benchmark
from quantx.btest.commission import AStockCommission
from quantx.btest.exch import Exch
from quantx.btest.data import Data
from quantx.btest.order import Order
from quantx.btest.portfolio import Portfolio
from quantx.btest.risk import Risk
from quantx.btest.scheduler import Scheduler, time_rule, date_rule
from quantx.btest.slippage import FixedSlippage
from quantx.btest.txn import SimulationTxn
from quantx.utils.const import DateFormat
from quantx.plotting import analyse as show_result


class SimulationExch(Exch):
    _benchmark = "000300.i"
    _starting_cash = 1000000
    _commission = AStockCommission()
    _risk = None
    _tqdm = None

    def __init__(self):
        Exch.__init__(self)

        self._txn = SimulationTxn()

    def __del__(self):
        if self._tqdm:
            self._tqdm.close()
        self._tqdm = None

    def open_order(self, order):
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

    def handle_order(self, order: Order):
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

            self._total_trades.append(txn)
            return txn
        except AssertionError as e:
            order.rejected(e)

            self._tqdm.write("[%s] %s SYMBOL:%s amount:%0.1f %s , %s" % (
                order.create_date.strftime(DateFormat.day),
                "BUY" if order.amount > 0 else "SELL",
                order.symbol,
                order.amount - order.deal_amount,
                order.status.upper(),
                order.error
            ))

    def handle_bar(self, context):
        self.portfolio.update(self._data)
        self._benchmark.handle(self, self._data)
        self._handle_bar(self, self._data)
        self._risk.calc(self.portfolio.returns, self._benchmark.returns)

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
            analyze=None,
            out_path=None
    ):

        self._handle_bar = handle_bar

        self._data = Data(self, start_date, end_date)

        self._scheduler = Scheduler(self._data.trading_day_lst)
        self._scheduler.add(self.handle_bar, date_rule.day(), time_rule.trading)

        if initialize:
            initialize(self)

        self._benchmark = Benchmark(self._benchmark, self._starting_cash)
        self._slippage = FixedSlippage()
        self._portfolio = Portfolio(self._starting_cash)
        self._risk = Risk()

        self._tqdm = tqdm(total=len(self._data.trading_day_lst), desc="backtesting")
        while not self._data.empty:
            for func in self._scheduler.get_funcs(self._data.trading_day):
                if func: func(self)

        results = DataFrame({
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
            results.to_pickle(out_path)

        for key, value in self._records.items():
            self._records[key] += [None] * (self.data.trading_day_ix - len(self._records[key]))
        dframe = DataFrame(self._records, index=self._data.trading_day_lst)
        results = concat([results, dframe], axis=1)

        if analyze:
            analyze(self, results)
        else:
            return results
