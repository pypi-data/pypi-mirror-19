from pandas import DataFrame

from quantx.btest.core import Exch
from quantx.btest.order import Order, MarketOrder
from quantx.btest.scheduler import time_rule, date_rule
from quantx.factors.factor import Factor, CustomFactor
from quantx.utils.config import Config
from quantx.utils.const import DateDefault, ModCls
from quantx.utils.factory import cls


def order(symbol, amount, style=None):
    style = style if style else MarketOrder()
    return style.shares(symbol, amount)


def order_value(symbol, amount, style=None):
    style = style if style else MarketOrder()
    return style.cash(symbol, amount)


def order_percent(symbol, amount, style=None):
    style = style if style else MarketOrder()
    return style.portfolio_percent(symbol, amount)


def order_target(symbol, amount, style=None):
    style = style if style else MarketOrder()
    return style.target_position(symbol, amount)


def order_target_value(symbol, amount, style=None):
    style = style if style else MarketOrder()
    return style.target_market_value(symbol, amount)


def order_target_percent(symbol, percent, style=None):
    style = style if style else MarketOrder()
    return style.target_portfolio_percent(symbol, percent)


def order_lots(symbol, amount, style=None):
    style = style if style else MarketOrder()
    return style.lots(symbol, amount)


def cancel_order(order: Order):
    return order.cancel()


def get_open_orders(symbol):
    return Exch.get_context().get_open_orders(symbol)


def get_order(order: Order):
    return Exch.get_context().get_order(order)


def scheduler_function(func, date=date_rule.day(), time=time_rule.before_trading):
    return Exch.get_context().scheduler.add(func, date, time)


def set_universe(*symbols):
    Exch.get_context().symbols = symbols


def f(name):
    return Factor(name)


def write_pipeline(name, factors, start_date=DateDefault.start, end_date=DateDefault.end, engine=Config.container):
    container = cls(engine, ModCls.container)(Exch.get_context().data.source, factors, start_date, end_date)
    Exch.get_context().pipeline.add(name, container)


def read_pipeline(name, symbols=slice(None), count=1) -> DataFrame:
    container = Exch.get_context().pipeline.get(name)
    trading_day = Exch.get_context().data.trading_day
    return container.history(trading_day,symbols,count)


def custom_f(f_func):
    def _f_func(*args, **kwargs):
        return CustomFactor(f_func, *args, **kwargs)

    return _f_func
