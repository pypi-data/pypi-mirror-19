from pandas import DataFrame, Series, to_datetime,IndexSlice

from quantx.datas.dataset import DataSet
from quantx.datas.source import Source
from quantx.factors.bundle import MarketBundle
from quantx.utils.config import Config
from quantx.utils.const import ModCls, Orient, Bar
from quantx.utils.factory import cls


class Data:
    _trading_days = None
    _bar_frame = None
    _bar_lst = None
    _bar_count = 0
    _dataset = None
    _source = None
    _context = None

    def __init__(self, context, start_date, end_date):
        self._context = context
        start_date = to_datetime(start_date)
        end_date = to_datetime(end_date)

        self._dataset = cls(Config.db, ModCls.dataset)(Config.get_db())
        self._source = cls(Config.source, ModCls.source)()
        self._source.update_trading_days()
        self._source.update_market(start_date, end_date)

        self._trading_days = self._dataset.get_trading_days(start_date, end_date).tolist()
        if not self._trading_days:
            return

        start_date, end_date = self._trading_days[0], self._trading_days[-1]

        self._bar_frame = self._dataset.get_bundle(MarketBundle, start_date, end_date)
        self._bar_lst = self._dataset.get_bundle(MarketBundle, start_date, end_date, orient=Orient.list)

    @property
    def store(self) -> DataSet:
        return self._dataset

    @property
    def source(self) -> Source:
        return self._source

    @property
    def trading_day(self):
        return self._trading_days[self._bar_count]

    @property
    def trading_day_ix(self):
        return self._bar_count

    @property
    def trading_day_lst(self) -> list:
        return self._trading_days

    @property
    def EOF(self):
        return self._bar_count >= self._trading_days.__len__()

    def current(self, symbols=None, columns=None):
        return self.history(symbols, columns).reset_index(0, drop=True)

    def history(self, symbols=slice(None), columns=slice(None), count=1) -> DataFrame:
        trading_days = self._trading_days[
                       self._bar_count - count
                       if self._bar_count - count > 0
                       else 0:self._bar_count + 1]
        return self._bar_frame.loc[IndexSlice[trading_days, symbols], columns]

    def can_trade(self, symbols=None) -> Series:
        assert symbols, "参数不能为空"
        return self.current(symbols, [Bar.active])[Bar.active]

    def is_stale(self, symbols=None):
        assert symbols, "参数不能为空"
        can_trade = self.can_trade(symbols).to_dict()

        def check(symbol):
            return True if self._context.traded_dict.__contains__(symbol) and not can_trade[symbol] else False

        if isinstance(symbols, (list, tuple)):
            result_dict = dict()
            for symbol in symbols:
                result_dict[symbol] = check(symbol)
            return Series(result_dict)

        return check(symbols)

    def get_quote(self, symbol, offset=0):
        return self.get_bar(symbol, offset)[Bar.close]

    def get_volume(self, symbol, offset=0):
        return self.get_bar(symbol, offset)[Bar.volume]

    def get_lot(self, symbol, offset=0):
        return 100  # self.get_bar(symbol, offset)[Bar.lot] todo 追加手数数据

    def is_stop(self, symbol, offset=0):
        return not self.get_bar(symbol, offset)[Bar.active]

    def get_limit(self, symbol):
        return 0.1  # todo 追加涨跌停幅度数据

    def get_bar(self, symbol=None, offset=0) -> dict:
        assert offset <= 0
        bar_count = self._bar_count + offset if self._bar_count >= abs(offset) else 0
        if not symbol:
            return self._bar_lst[bar_count]
        return self._bar_lst[bar_count][symbol]

    def next(self):
        self._bar_count += 1
