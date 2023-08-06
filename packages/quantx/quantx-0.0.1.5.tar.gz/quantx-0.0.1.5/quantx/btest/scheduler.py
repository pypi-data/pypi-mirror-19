from enum import Enum
from queue import Queue

from pandas.tslib import Timestamp

from quantx.utils.const import Freq


class date_rule(object):
    @staticmethod
    def year(trading_day=1):
        return Freq.A, trading_day

    @staticmethod
    def quarter(trading_day=1):
        return Freq.Q, trading_day

    @staticmethod
    def month(trading_day=1):
        return Freq.M, trading_day

    @staticmethod
    def week(trading_day=1):
        return Freq.W, trading_day

    @staticmethod
    def day():
        return Freq.D, 1


class time_rule(Enum):
    before_trading = 1
    after_trading = 2
    trading = 3  # todo 拆分:分钟,小时,半天


class Scheduler:
    _trading_days = None
    _start_date = None
    _end_date = None
    _freq = None
    _events = dict()
    _count_dict = dict()
    _queue = Queue()

    def __init__(self, trading_days: list):
        for t in time_rule:
            self._events[t] = dict()
            for d in Freq:
                self._events[t][d] = list()

        for d in Freq:
            self._count_dict[d] = dict()

        self.update(trading_days)

    def add(self, func, date, time=time_rule.before_trading):
        assert date[1] != 0
        self._events[time][date[0]].append((date[1], func))

    def _handle_t(self, now: Timestamp, time):
        for date, func_lst in self._events[time].items():
            for trading_day, func in func_lst:
                _count = self._get_count(date, now)
                if date == Freq.D:
                    self._queue.put(func)
                elif abs(trading_day) <= _count.__len__() and now == _count[trading_day]:
                    self._queue.put(func)

    def update(self, trading_days: list):
        def update(now, date, label):
            lst = self._count_dict[date].get(label, [])
            lst.append(now)
            self._count_dict[date][label] = lst

        for now in trading_days:
            update(now, Freq.A, now.year)
            update(now, Freq.Q, "Q_%s_%s" % (now.year, now.quarter))
            update(now, Freq.M, "M_%s_%s" % (now.year, now.month))
            update(now, Freq.W, "W_%s_%s" % (now.year, now.weekofyear))
            update(now, Freq.D, "D")

    def _get_count(self, date, now: Timestamp) -> list:
        if date == Freq.A:
            return self._count_dict[Freq.A][now.year]
        elif date == Freq.Q:
            return self._count_dict[Freq.Q]["%s_%s" % (now.year, now.quarter)]
        elif date == Freq.M:
            return self._count_dict[Freq.M]["%s_%s" % (now.year, now.month)]
        elif date == Freq.W:
            return self._count_dict[Freq.W]["%s_%s" % (now.year, now.weekofyear)]
        elif date == Freq.D:
            return self._count_dict[Freq.D]["D"]

    def get_funcs(self, now: Timestamp):
        self._handle_t(now, time_rule.before_trading)
        self._handle_t(now, time_rule.trading)
        self._handle_t(now, time_rule.after_trading)

        while not self._queue.empty():
            yield self._queue.get()


if __name__ == "__main__":
    from quantx import SimulationExch

    SimulationExch()._run(None)
