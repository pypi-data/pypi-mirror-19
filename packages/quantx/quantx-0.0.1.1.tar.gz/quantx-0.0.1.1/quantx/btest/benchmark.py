from quantx.btest.returns import Returns


class Benchmark:
    _symbol = None
    _capital = 0
    _position = 0
    returns = None
    _last_value = None
    _value = None

    def __init__(self, symbol, capital):
        self._symbol = symbol
        self._capital = capital
        self._position = 0
        self.returns = Returns(capital)

    def update(self, trading_day, quote):
        if not self._last_value:
            self._position = self._capital // quote[self._symbol] // 100 * 100
            self._last_value = self._position * quote[self._symbol]

        value = self._position * quote[self._symbol]

        self.returns.update(trading_day, self._last_value, value)

        self._last_value = value
