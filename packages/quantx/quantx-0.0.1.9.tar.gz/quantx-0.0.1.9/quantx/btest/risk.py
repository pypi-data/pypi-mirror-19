import numpy

from quantx.btest.returns import Returns
from quantx.utils.const import DateDefault


class Risk:
    _rf_rate = 0
    _volatility_lst = []
    _max_drawdown_lst = []
    _tracking_error_lst = []
    _information_rate_lst = []
    _beta_lst = []
    _alpha_lst = []
    _downside_risk_lst = []
    _sortino_lst = []
    _sharpe_lst = []

    @property
    def volatility_lst(self):
        return self._volatility_lst

    @property
    def max_drawdown_lst(self):
        return self._max_drawdown_lst

    @property
    def tracking_error_lst(self):
        return self._tracking_error_lst

    @property
    def information_rate_lst(self):
        return self._information_rate_lst

    @property
    def beta_lst(self):
        return self._beta_lst

    @property
    def alpha_lst(self):
        return self._alpha_lst

    @property
    def downside_risk_lst(self):
        return self._downside_risk_lst

    @property
    def sortino_lst(self):
        return self._sortino_lst

    @property
    def sharpe_lst(self):
        return self._sharpe_lst

    @property
    def volatility(self):
        return self._volatility_lst[-1]

    @volatility.setter
    def volatility(self, value):
        self._volatility_lst.append(value)

    @property
    def max_drawdown(self):
        return self._max_drawdown_lst[-1] if self._max_drawdown_lst else 0

    @max_drawdown.setter
    def max_drawdown(self, value):
        self._max_drawdown_lst.append(value)

    @property
    def tracking_error(self):
        return self._tracking_error_lst[-1]

    @tracking_error.setter
    def tracking_error(self, value):
        self._tracking_error_lst.append(value)

    @property
    def information_rate(self):
        return self._information_rate_lst[-1]

    @information_rate.setter
    def information_rate(self, value):
        self._information_rate_lst.append(value)

    @property
    def beta(self):
        return self._beta_lst[-1]

    @beta.setter
    def beta(self, value):
        self._beta_lst.append(value)

    @property
    def alpha(self):
        return self._alpha_lst[-1]

    @alpha.setter
    def alpha(self, value):
        self._alpha_lst.append(value)

    @property
    def downside_risk(self):
        return self._downside_risk_lst[-1]

    @downside_risk.setter
    def downside_risk(self, value):
        self._downside_risk_lst.append(value)

    @property
    def sortino(self):
        return self._sortino_lst[-1]

    @sortino.setter
    def sortino(self, value):
        self._sortino_lst.append(value)

    @property
    def sharpe(self):
        return self._sharpe_lst[-1]

    @sharpe.setter
    def sharpe(self, value):
        self._sharpe_lst.append(value)

    def calc(self, rets: Returns, benchmark_rets: Returns):
        daily_rets_lst = numpy.array(rets.daily_lst)
        benchmark_rets_lst = numpy.array(benchmark_rets.daily_lst)
        diff = daily_rets_lst - benchmark_rets_lst
        cov = numpy.cov(numpy.vstack([daily_rets_lst, benchmark_rets_lst]), ddof=1)
        mask = daily_rets_lst < benchmark_rets_lst
        mask_diff = daily_rets_lst[mask] - benchmark_rets_lst[mask]

        self.volatility = DateDefault.year ** 0.5 * numpy.std(rets.daily_lst, ddof=1)
        self.max_drawdown = min(self.max_drawdown, (1 + rets.total) / (1 + rets.max) - 1)
        self.tracking_error = ((diff * diff).sum() / len(diff)) ** 0.5 * DateDefault.year ** 0.5
        self.information_rate = (rets.annual - benchmark_rets.annual) / self.volatility
        self.beta = cov[0][1] / cov[1][1]
        self.alpha = rets.annual - (self._rf_rate + self.beta) * (benchmark_rets.annual - self._rf_rate)
        self.downside_risk = ((mask_diff * mask_diff).sum() / len(mask_diff)) ** 0.5 * DateDefault.year ** 0.5
        self.sortino = (rets.annual - self._rf_rate) / self.downside_risk
        self.sharpe = (rets.annual - self._rf_rate) / self.volatility
