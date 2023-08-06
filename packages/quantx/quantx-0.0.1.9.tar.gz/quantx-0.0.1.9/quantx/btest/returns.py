from quantx.utils.const import DateDefault


class Returns:
    _daily_lst = None
    _total_lst = None
    _max_lst = None
    _annual_lst = None
    _starting_cash = None
    _start_date = None

    @property
    def daily_lst(self):
        return self._daily_lst

    @property
    def total_lst(self):
        return self._total_lst

    @property
    def max_lst(self):
        return self._max_lst

    @property
    def annual_lst(self):
        return self._annual_lst

    @property
    def daily(self):
        return self._daily_lst[-1] if self._daily_lst else 0

    @daily.setter
    def daily(self, value):
        self._daily_lst.append(value)

    @property
    def total(self):
        return self._total_lst[-1] if self._total_lst else 0

    @total.setter
    def total(self, value):
        self._total_lst.append(value)

    @property
    def max(self):
        return self._max_lst[-1] if self._max_lst else 0

    @max.setter
    def max(self, value):
        self._max_lst.append(value)

    @property
    def annual(self):
        return self._annual_lst[-1] if self._annual_lst else 0

    @annual.setter
    def annual(self, value):
        self._annual_lst.append(value)

    def __init__(self, starting_cash):
        self._starting_cash = starting_cash
        self._daily_lst = []
        self._total_lst = []
        self._max_lst = []
        self._annual_lst = []

    def update(self, trading_day, last_value, value):
        if not self._start_date:
            self._start_date = trading_day

        self.daily = (value - last_value) / last_value
        self.total = value / self._starting_cash - 1
        self.max = max(self.total, self.max)
        self.annual = (1 + self.total) ** (DateDefault.year / ((trading_day - self._start_date).days + 1)) - 1
