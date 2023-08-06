from datetime import timedelta

from quantx.datas.dataset import DataSet
from quantx.factors.factor import Factor
from quantx.utils import convert
from quantx.utils import dl
from quantx.utils.config import Config
from quantx.utils.const import DateDefault, ModCls, DateFormat, DataCol, DataFill
from quantx.utils.convert import ts, dt
from quantx.utils.factory import cls
from pandas import concat


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

    def _factor(self, factor, start_date, end_date):
        return self._get_url("http://192.168.1.19:8099/data/factor", {
            "from": start_date,
            "to": end_date,
            "factors": factor.name
        })

    def _market(self, start_date, end_date, index=False):
        url = "http://192.168.1.19:8099/data/price"
        return self._get_url(url + "/index" if index else url, {
            "code": "000300",
            "from": start_date,
            "to": end_date
        })

    def _dividend(self, start_date, end_date, ):
        return self._get_url("http://192.168.1.19:8099/data/bonus", {
            "from": start_date,
            "to": end_date
        })

    def _csv_file(self, *args):
        return "_".join([str(arg) for arg in args]) + ".csv"

    def get(self, bundle_factor, start_date, end_date):
        start_date = dt(start_date).strftime(DateFormat.day)
        end_date = dt(end_date).strftime(DateFormat.day)
        flabel = lambda l: "_".join([l, start_date, end_date])

        if isinstance(bundle_factor, Factor):
            factor = dl.download_csv(
                self._factor(bundle_factor, start_date, end_date), flabel(bundle_factor.name)
            ).rename(columns={"tick": DataCol.symbol, "date": DataCol.dt})

            factor[DataCol.symbol] = factor.symbol.apply(convert.symbol)
            return factor

        market = dl.download_csv(
            self._market(start_date, end_date), flabel(bundle_factor.name)
        ).rename(columns={"tick": "symbol", "stop": "active"})
        market["active"] = market.active.apply(lambda x: not x)
        market["symbol"] = market.symbol.apply(convert.symbol)

        index = dl.download_csv(
            self._market(start_date, end_date, index=True), flabel("index")
        ).rename(columns={"tick": "symbol"})
        index["active"] = True
        index["symbol"] = index.symbol.apply(convert.index)
        market = market.append(index)

        dividend = dl.download_csv(
            self._dividend(start_date, end_date), flabel("dividend")
        ).rename(columns={"tick": "symbol"})
        dividend["symbol"] = dividend.symbol.apply(convert.symbol)

        market["lot"] = 100
        market["limit"] = 10

        return concat([
            market.set_index(["dt", "symbol"]),
            dividend.set_index(["dt", "symbol"])],
            axis=1
        ).fillna(0).reset_index()


