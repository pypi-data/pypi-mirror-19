import os
from datetime import datetime

import bcolz
import numpy
import pandas
import shutil
from bcolz import carray
from pandas import DataFrame
from pandas import HDFStore
from pandas import Series
from pandas import read_hdf
from tqdm import tqdm

from quantx.datas.cache import Cache
from quantx.factors.bundle import Bundle
from quantx.factors.factor import Factor
from quantx.utils import convert
from quantx.utils.config import Config
from quantx.utils.const import Orient, DataCol, DateFormat, DataType, DateDefault, ModCls
from quantx.utils.factory import cls


class DataSet:
    _trading_days = None

    @property
    def cache(self) -> Cache:
        return self._trading_days

    def update_factor(self, factor, dt_col=DataCol.dt, symbol_col=DataCol.symbol):
        raise NotImplementedError

    def get_factor(self, factor, start_date=DateDefault.start, end_date=DateDefault.end, dtype=None) -> Series:
        raise NotImplementedError

    def get_factor_start(self, factor, stat_date=DateDefault.start):
        raise NotImplementedError

    def get_factor_end(self, factor, end_date=DateDefault.end):
        raise NotImplementedError

    def update_bundle(self, dframe: DataFrame, bundle: Bundle, dt_col=DataCol.dt, symbol_col=DataCol.symbol):
        raise NotImplementedError

    def get_bundle(self, bundle: Bundle, start_date=DateDefault.start, end_date=DateDefault.end,
                   orient=Orient.dframe) -> DataFrame:
        raise NotImplementedError

    def get_bundle_start(self, bundle: Bundle):
        raise NotImplementedError

    def get_bundle_end(self, bundle: Bundle):
        raise NotImplementedError

    def update_trading_days(self, trading_days: Series):
        raise NotImplementedError

    def get_trading_days(self, start_date, end_date) -> Series:
        raise NotImplementedError

    def drop(self, bundle_factor):
        raise NotImplementedError

    def _format_bundle(self, dframe, bundle):
        for name in dir(bundle):
            factor = getattr(bundle, name)
            if isinstance(factor, Factor):
                column = factor.inputs[0].split(".")[1]
                dframe[column] = dframe[column].astype(factor.dtype)
        return dframe

    def _convert_list(self, dframe) -> list:
        panel = dframe.to_panel()
        tqdm.pandas(desc="unpacking")

        return panel.progress_apply(
            lambda x: x.to_dict(), axis=0
        ).apply(
            lambda x: x.to_dict(), axis=1
        ).tolist()


class LocalDataSet(DataSet):
    def __init__(self, uri, cache=Config.cache_db):
        self.uri = uri
        self._trading_days = DataFrame()  # cls(cache, ModCls.cache)(uri)
        self._cache = cls(cache, ModCls.cache)(uri)

    def update_factor(self, factor, dt_col=DataCol.dt, symbol_col=DataCol.symbol, append=True):
        factor.rename(columns={dt_col: DataCol.dt, symbol_col: DataCol.symbol}, inplace=True)
        if factor[DataCol.dt].dtype.type != numpy.datetime64:
            factor[DataCol.dt] = factor[DataCol.dt].astype(numpy.datetime64)
        name = set(factor.columns).difference([DataCol.dt, DataCol.symbol]).pop()

        with HDFStore(self.uri) as hdf:
            hdf.put(name, factor.set_index(DataCol.dt), "t", append=append)
            hdf.flush(True)

    def get_factor(self, factor, start_date=DateDefault.start, end_date=DateDefault.end, dtype=None):
        with HDFStore(self.uri) as hdf:
            assert hdf.__contains__(factor), "不存在因子[%s],请先更新" % factor

            start_date = start_date.strftime(DateFormat.day)
            end_date = end_date.strftime(DateFormat.day)

            cache_name = "%s_%s_%s" % (factor, start_date, end_date)

            ser = self._cache.get(cache_name)

            if not isinstance(ser, Series):
                ser = hdf.select(
                    factor,
                    where=[
                        "index >= '%s'" % (start_date),
                        "index <= '%s'" % (end_date)
                    ]
                ).reset_index()

                ser = ser.set_index([
                    DataCol.dt,
                    DataCol.symbol
                ])[factor].astype(dtype).sort_index()

                self._cache.set(cache_name, ser)

            return ser

    def get_factor_start(self, factor, start_date=DateDefault.start):
        try:
            dframe = read_hdf(self.uri, factor, start=0, stop=1)
            return pandas.to_datetime(dframe.iloc[-1].name)
        except (KeyError, IOError):
            return None

    def get_factor_end(self, factor, end_date=DateDefault.end):
        try:
            dframe = read_hdf(self.uri, factor, start=-1)
            return pandas.to_datetime(dframe.iloc[-1].name)
        except (KeyError, IOError):
            return None

    def update_bundle(self, dframe: DataFrame, bundle: Bundle, dt_col=DataCol.dt, symbol_col=DataCol.symbol):
        dframe.rename(columns={dt_col: DataCol.dt, symbol_col: DataCol.symbol}, inplace=True)
        dframe[DataCol.dt] = dframe[DataCol.dt].astype(numpy.datetime64)

        with HDFStore(self.uri) as hdf:
            hdf.put(convert.cls_tab(bundle), dframe.set_index(dt_col), "t", append=True)
            dframe = hdf[convert.cls_tab(bundle)].reset_index().set_index([
                DataCol.dt,
                DataCol.symbol
            ], drop=False)

            bundle_list = self._convert_list(dframe)
            ca = carray(bundle_list, rootdir=Config.get_root_file(convert.cls_tab(bundle)), mode="w")
            ca.flush()
            hdf.flush(True)

    def get_bundle_start(self, bundle):
        try:
            dframe = read_hdf(self.uri, convert.cls_tab(bundle), start=0, stop=1)
            return pandas.to_datetime(dframe.iloc[0].name)
        except (KeyError, IOError):
            return None

    def get_bundle_end(self, bundle: Bundle):
        try:
            dframe = read_hdf(self.uri, convert.cls_tab(bundle), start=-1)
            return pandas.to_datetime(dframe.iloc[-1].name)
        except (KeyError, IOError):
            return None

    def get_bundle(self, bundle: Bundle, start_date=DateDefault.start, end_date=DateDefault.end, orient=Orient.dframe):
        if orient == Orient.dframe:
            dframe = read_hdf(self.uri, convert.cls_tab(bundle), where=[
                "index >= '%s'" % (start_date.strftime(DateFormat.day)),
                "index <= '%s'" % (end_date.strftime(DateFormat.day))
            ]).reset_index()

            return dframe.set_index([
                DataCol.dt,
                DataCol.symbol
            ]).sort_index()


        elif orient == Orient.list:
            market_start = self.get_bundle_start(bundle)
            trading_days = self.get_trading_days(start_date, end_date)

            start_ix = (trading_days.iloc[0] - market_start).days
            end_ix = start_ix + (trading_days.iloc[-1] - trading_days.iloc[0]).days + 1
            bundle_list = bcolz.open(Config.get_root_file(convert.cls_tab(bundle)), mode="r")
            return list(bundle_list.iter(start=start_ix, limit=end_ix))

    def update_trading_days(self, trading_days: Series):
        trading_days.name = DataCol.dt
        trading_days.to_hdf(self.uri, DataType.trading_days)

    def get_trading_days(self, start_date=None, end_date=None) -> Series:
        cache_name = "%s_%s_%s" % (DataType.trading_days, start_date, end_date)
        data = self._cache.get(cache_name)
        if not isinstance(data, Series):
            data = read_hdf(
                self.uri, DataType.trading_days
            ).astype(numpy.datetime64)
            data = data[data >= start_date] if start_date else data
            data = data[data <= end_date] if end_date else data
            self._cache.set(cache_name, data)

        return data

    def drop(self, bundle_factor):
        with pandas.HDFStore(self.uri) as hdf:
            hdf.remove(bundle_factor)

        if os.path.isdir(Config.get_root_file(bundle_factor)):
            shutil.rmtree(Config.get_root_file(bundle_factor))

if __name__ == '__main__':
    lds = LocalDataSet("d:/work/data/quantx/local.db")
    print(lds.get_factor("M001007", datetime(2016, 1, 25)))
