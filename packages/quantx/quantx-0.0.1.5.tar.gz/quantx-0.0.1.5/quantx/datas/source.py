import os
from datetime import timedelta, datetime

import pandas
from pandas import DataFrame, Series

from quantx.datas.dataset import DataSet
from quantx.factors.bundle import MarketBundle
from quantx.factors.factor import Factor
from quantx.utils import convert
from quantx.utils import dl
from quantx.utils.config import Config
from quantx.utils.const import DateDefault, ModCls, DateFormat, DataCol, DataFill
from quantx.utils.convert import ts, dt
from quantx.utils.factory import cls


class Source:
    _dataset = cls(Config.db, ModCls.dataset)(Config.get_db())

    @property
    def store(self) -> DataSet:
        return self._dataset

    def get(self, bundle_factor, start_date, end_date):
        raise NotImplementedError

    def update(self, bundle_factor, start_date=DateDefault.start, end_date=DateDefault.end):
        start, end = self.store.get_anchor(bundle_factor)

        if not start and not end:
            self.store.update(
                bundle_factor,
                self.get(bundle_factor, start_date, end_date),
                anchor=(ts(start_date), ts(end_date))
            )
        else:
            if ts(start_date) < start:
                self.store.update(
                    bundle_factor,
                    self.get(bundle_factor, start_date, dt(start) - timedelta(days=1)),
                    anchor=(ts(start_date), end),
                    dfill=DataFill.head
                )
                start = ts(start_date)

            if ts(end_date) > end:
                self.store.update(
                    bundle_factor,
                    self.get(bundle_factor, dt(end) + timedelta(days=1), end_date),
                    anchor=(start, ts(end_date)),
                    dfill=DataFill.tail
                )


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
            "factors": factor.name
        })

    def _market(self, start_date=None, end_date=None):
        return self._get_url("http://192.168.1.19:8099/data/price", {
            "from": start_date,
            "to": end_date
        })

    def _csv_file(self, *args):
        return "_".join([str(arg) for arg in args]) + ".csv"

    def get(self, bundle_factor, start_date, end_date):
        label = "_".join([
            bundle_factor.name,
            dt(start_date).strftime(DateFormat.day),
            dt(end_date).strftime(DateFormat.day)])

        if isinstance(bundle_factor, Factor):
            dframe = dl.download_csv(self._factor(bundle_factor,
                    dt(start_date).strftime(DateFormat.day),
                    dt(end_date).strftime(DateFormat.day)),label
            ).rename(columns={"tick": DataCol.symbol, "date": DataCol.dt})

            dframe[DataCol.symbol] = dframe.symbol.apply(convert.symbol)
            return dframe

        dframe = dl.download_csv(
            self._market(
                dt(start_date).strftime(DateFormat.day),
                dt(end_date).strftime(DateFormat.day)
            ), label
        ).reset_index().rename(columns={"tick": "symbol", "stop": "active"})

        dframe["active"] = dframe.active.apply(lambda x: not x)
        dframe["symbol"] = dframe.symbol.apply(convert.symbol)
        dframe.drop("index", axis=1, inplace=True)

        return dframe


if __name__ == '__main__':
    from datetime import datetime

    css = ChinaScopeSource()
    css.update(Factor("M001007"), "2016-01-01", "2016-01-15")
    css.update(Factor("M001012"), "2016-01-01", "2016-01-15")
