from pandas import DataFrame, Series, to_datetime, IndexSlice

from quantx.datas.dataset import DataSet
from quantx.datas.source import Source
from quantx.factors.bundle import MarketBundle
from quantx.utils.config import Config
from quantx.utils.const import ModCls, Orient, Bar
from quantx.utils.factory import cls


class Data:
    _bar_count = 0
    _dataset = None
    _source = None
    _context = None
    _bars = None
    _cache = dict()

    def __init__(self, context, start_date, end_date):
        self._context = context
        start_date = to_datetime(start_date)
        end_date = to_datetime(end_date)

        self._dataset = cls(Config.db, ModCls.dataset)(Config.get_db())
        self._source = cls(Config.source, ModCls.source)()
        self._source.update(MarketBundle, start_date, end_date)

        self._bars = self._dataset.get(MarketBundle, start_date, end_date)

    @property
    def store(self) -> DataSet:
        return self._dataset

    @property
    def source(self) -> Source:
        return self._source

    @property
    def trading_day(self):
        return self.trading_day_lst[self._bar_count]

    @property
    def trading_day_ix(self):
        return self._bar_count

    @property
    def trading_day_lst(self) -> list:
        return self._bars.dts

    @property
    def empty(self):
        return self._bar_count >= len(self._bars)

    @property
    def symbols(self) -> list:
        return self._bars.symbols

    def _get_bar_field(self, symbol, field, td=0):
        return self._bars[
            self._bar_count + td if td <= 0 else self._bar_count,
            field,
            symbol
        ]

    def get_quote(self, symbol, td=0):
        return self._get_bar_field(symbol, Bar.quote, td)

    def get_inc(self, symbol, td=0):
        return self._get_bar_field(symbol, Bar.inc, td)

    def get_volume(self, symbol, td=0):
        return self._get_bar_field(symbol, Bar.volume, td)

    def is_stop(self, symbol, td=0):
        return not self._get_bar_field(symbol, Bar.active, td)

    def last(self, field=None, symbol=None):
        return self.history(1, field, symbol)

    def history(self, bar_count, field=None, symbol=None):
        start = self._bar_count - bar_count if self._bar_count - bar_count > 0 else 0
        stop = self._bar_count + 1

        if bar_count == 1 or stop - start == 1:
            if not field and not symbol:
                return DataFrame(
                    self._bars[self._bar_count],
                    index=self._bars.fields,
                    columns=self._bars.symbols
                )
            elif not field:
                return Series(
                    self._bars[self._bar_count, :, symbol],
                    index=self._bars.fields,
                    name=symbol
                )
            elif not symbol:
                return Series(
                    self._bars[self._bar_count, field, :],
                    index=self._bars.symbols,
                    name=symbol
                )
            elif bar_count == 1:
                return self._bars[self._bar_count, field, symbol]
            else:
                return self._bars[start:stop, field, symbol]
        elif field and symbol:
            return self._bars[start:stop, field, symbol]
        elif field:
            return DataFrame(
                self._bars[start:stop, field, :],
                index=self._bars.dts[start:stop],
                columns=self._bars.symbols
            )
        elif symbol:
            return DataFrame(
                self._bars[start:stop, :, symbol],
                index=self._bars.dts[start:stop],
                columns=self._bars.fields
            )

    # def can_trade(self, symbols=None) -> Series:
    #     assert symbols, "参数不能为空"
    #     return self.current(symbols, Bar.active)[Bar.active]
    #
    # def is_stale(self, symbols=None):
    #     assert symbols, "参数不能为空"
    #     can_trade = self.can_trade(symbols).to_dict()
    #
    #     def check(symbol):
    #         return True if self._context.traded_dict.__contains__(symbol) and not can_trade[symbol] else False
    #
    #     if isinstance(symbols, (list, tuple)):
    #         result_dict = dict()
    #         for symbol in symbols:
    #             result_dict[symbol] = check(symbol)
    #         return Series(result_dict)
    #
    #     return check(symbols)

    def get_lot(self, symbol, offset=0):
        return 100  # self.get_bar(symbol, offset)[Bar.lot] todo 追加手数数据

    def get_limit(self, symbol):
        return 10  # todo 追加涨跌停幅度数据

    def next(self):
        self._bar_count += 1
