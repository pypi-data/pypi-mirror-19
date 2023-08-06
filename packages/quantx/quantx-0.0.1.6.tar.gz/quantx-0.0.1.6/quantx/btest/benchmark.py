from quantx.btest.data import Data

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

    def handle(self, context, data: Data):
        bar = data.get_bar(self._symbol)
        if not self._last_value:
            self._position = self._capital / bar.close
            self._last_value = self._position * bar.close

        value = self._position * bar.close

        self.returns.update(data.trading_day, self._last_value, value)

        self._last_value = value
