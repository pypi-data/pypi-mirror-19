import os
from datetime import timedelta, datetime

import pandas
from pandas import DataFrame, Series

from quantx.datas.dataset import DataSet
from quantx.factors.bundle import MarketBundle
from quantx.utils import convert
from quantx.utils import dl
from quantx.utils.config import Config
from quantx.utils.const import DateDefault, ModCls, DateFormat, DataType, DataCol
from quantx.utils.factory import cls


class Source:
    _dataset = cls(Config.db, ModCls.dataset)(Config.get_db())

    @property
    def store(self) -> DataSet:
        return self._dataset

    def get_factor(self, factor, start_date, end_date) -> Series:
        raise NotImplementedError

    def get_market(self, start_date, end_date) -> DataFrame:
        raise NotImplementedError

    def get_trading_days(self, start_date, end_date) -> Series:
        raise NotImplementedError

    def update_trading_days(self):
        lastest_updated = pandas.to_datetime(Config.latest_updated)
        diff = (datetime.now() - lastest_updated)
        if diff.days >= 1 or not os.path.isfile(Config.get_db()):
            ser = self.get_trading_days(DateDefault.start, DateDefault.end + timedelta(days=1))
            self.store.update_trading_days(ser)
            Config.latest_updated = datetime.now().strftime(DateFormat.day)
            Config.save()

    def update_market(self, start_date=DateDefault.start, end_date=DateDefault.end):
        market_start = self.store.get_bundle_start(MarketBundle)
        market_end = self.store.get_bundle_end(MarketBundle)
        trading_days = self.store.get_trading_days(start_date, end_date)

        if trading_days.empty:
            return

        if not market_start or not market_end:
            market_data = self.get_market(trading_days.iloc[0], trading_days.iloc[-1])
            self.store.update_bundle(market_data, MarketBundle)
        elif trading_days.iloc[0] < market_start:
            self.store.drop(convert.cls_tab(MarketBundle))
            self.store.update_bundle(self.get_market(trading_days.iloc[0], trading_days.iloc[-1]), MarketBundle)
        elif trading_days.iloc[-1] > market_end:
            self.store.update_bundle(self.get_market(market_end + timedelta(days=1), end_date), MarketBundle)

    def update_factor(self, factor, start_date=DateDefault.start, end_date=DateDefault.end):
        factor_start = self.store.get_factor_start(factor, start_date)
        factor_end = self.store.get_factor_end(factor, end_date)
        start_date = pandas.to_datetime(start_date)
        end_date = pandas.to_datetime(end_date)

        if not factor_start or not factor_end:
            self.store.update_factor(self.get_factor(factor, start_date, end_date))
        elif start_date < factor_start:
            self.store.drop(factor)
            self.store.update_factor(self.get_factor(factor, start_date, end_date))
        elif end_date > factor_end:
            self.store.update_factor(self.get_factor(factor, factor_end + timedelta(days=1), end_date))


class ChinaScopeSource(Source):
    def _get_url(self, url, params: dict):
        param_lst = []

        for key, value in params.items():
            if not value:
                continue
            param_lst.append(key + "=" + value)

        return url + "?" + "&".join(param_lst)

    def _factor(self, factor, start_date=None, end_date=None):
        return self._get_url("http://192.168.1.19:8099/data/factor", {
            "from": start_date,
            "to": end_date,
            "factors": factor
        })

    def _market(self, start_date=None, end_date=None):
        return self._get_url("http://192.168.1.19:8099/data/price", {
            "from": start_date,
            "to": end_date
        })

    def _trading_days(self, start_date, end_date):
        return self._get_url("http://192.168.1.19:8099/data/dates", {
            "from": start_date,
            "to": end_date
        })

    def _csv_file(self, *args):
        return "_".join([str(arg) for arg in args]) + ".csv"

    def get_factor(self, factor, start_date, end_date) -> Series:
        dframe = dl.download_csv(
            self._factor(factor, start_date.strftime(DateFormat.day), end_date.strftime(DateFormat.day)),
            factor
        ).rename(columns={"tick": DataCol.symbol, "date": DataCol.dt})

        dframe[DataCol.symbol] = dframe.symbol.apply(convert.symbol)
        return dframe

    def get_trading_days(self, start_date: datetime, end_date: datetime) -> Series:
        ser = dl.download_csv(self._trading_days(
            start_date.strftime(DateFormat.day),
            end_date.strftime(DateFormat.day)
        ), DataType.trading_days, dtype=Series)

        ser.name = DataCol.dt
        return ser

    def get_market(self, start_date: datetime, end_date: datetime) -> DataFrame:
        dframe = dl.download_csv(
            self._market(
                start_date.strftime(DateFormat.day),
                end_date.strftime(DateFormat.day)),
            "market"
        ).reset_index().rename(columns={"tick": "symbol", "stop": "active"})

        dframe["active"] = dframe.active.apply(lambda x: not x)
        dframe["symbol"] = dframe.symbol.apply(convert.symbol)
        dframe.drop("index", axis=1, inplace=True)

        return dframe


if __name__ == '__main__':
    from datetime import datetime

    css = ChinaScopeSource()
    css.update_factor("M001007")
    css.update_factor("M001012")
