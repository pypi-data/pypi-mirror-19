from pandas import DataFrame

from quantx.btest.ctx import ExchContext
from quantx.btest.order import MarketOrder
from quantx.btest.scheduler import time_rule, date_rule
from quantx.factors.factor import Factor, CustomFactor
from quantx.utils.config import Config
from quantx.utils.const import DateDefault, ModCls
from quantx.utils.factory import cls


def order_shares(symbol, amount, style=None):
    style = style if style else MarketOrder()
    return style.shares(symbol, amount)


def order_value(symbol, cash_amount, style=None):
    style = style if style else MarketOrder()
    return style.cash(symbol, cash_amount)


def order_percent(symbol, percent, style=None):
    style = style if style else MarketOrder()
    return style.portfolio_percent(symbol, percent)


def order_target(symbol, amount, style=None):
    style = style if style else MarketOrder()
    return style.target_position(symbol, amount)


def order_target_value(symbol, cash_amount, style=None):
    style = style if style else MarketOrder()
    return style.target_market_value(symbol, cash_amount)


def order_target_percent(symbol, percent, style=None):
    style = style if style else MarketOrder()
    return style.target_portfolio_percent(symbol, percent)


def order_lots(symbol, amount, style=None):
    style = style if style else MarketOrder()
    return style.lots(symbol, amount)


def cancel_order(order_id):
    ExchContext.get_exch().get_order(order_id).cancel()


def get_open_orders():
    return ExchContext.get_exch().get_open_orders()


def get_order(order_id):
    return ExchContext.get_exch().get_order(order_id)


def scheduler_function(func, date=date_rule.day(), time=time_rule.before_trading):
    return ExchContext.get_exch().scheduler.add(func, date, time)


def update_universe(id_or_symbols):
    raise NotImplementedError


def instruments(id_or_symbols):
    raise NotImplementedError


def history(bar_count, field=None, symbol=None):
    return ExchContext.get_exch().data.history(bar_count, field, symbol)


def last(field, symbol):
    return ExchContext.get_exch().data.last(field, symbol)


def plot(series_name, value):
    pass


def f(name):
    return Factor(name)


def write_pipeline(name, factor, start_date=DateDefault.start, end_date=DateDefault.end, engine=Config.container):
    container = cls(engine, ModCls.container)(ExchContext.get_exch().data.source, factor, start_date, end_date)
    container.run()
    ExchContext.get_exch().pipeline.add(name, container)


def read_pipeline(name, bar_count, symbols=slice(None)) -> DataFrame:
    container = ExchContext.get_exch().pipeline.get(name)
    stop = ExchContext.get_exch().data.trading_day_ix + 1
    start = stop - bar_count if stop - bar_count >= 0 else 0
    assert start < stop
    return container.data.iloc[start:stop][symbols]


def custom_f(f_func):
    def _f_func(*args, **kwargs):
        return CustomFactor(f_func, *args, **kwargs)

    return _f_func


def record(**kwargs):
    ExchContext.get_exch().record(**kwargs)
