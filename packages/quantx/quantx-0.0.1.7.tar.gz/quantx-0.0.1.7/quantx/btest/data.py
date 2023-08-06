from collections import namedtuple

from pandas import DataFrame, Series, to_datetime

from quantx.datas.dataset import DataSet
from quantx.datas.source import Source
from quantx.utils.config import Config
from quantx.utils.const import ModCls, BundleCls
from quantx.utils.factory import cls

Bar = namedtuple(
    "Bar",
    ["open", "high", "low", "close", "vol", "inc", "bns", "abns", "active", "givsr", "lot", "limit"]
)


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
        self._source.update(cls(BundleCls.market, ModCls.bundle), start_date, end_date)

        self._bars = self._dataset.get(cls(BundleCls.market, ModCls.bundle), start_date, end_date)

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

    def get_bar(self, symbol, td=0):
        return Bar(**Series(
            self._bars[self._bar_count + td if td <= 0 else self._bar_count, :, symbol],
            index=self._bars.fields
        ))

    def is_stop(self, symbol, td=0):
        return not self.get_bar(symbol, td).active

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

    def next(self):
        self._bar_count += 1
