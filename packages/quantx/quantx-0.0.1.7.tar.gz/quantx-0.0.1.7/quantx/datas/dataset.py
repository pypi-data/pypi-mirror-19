import os

import bcolz
import numpy
import pandas
import shutil
from bcolz import carray
from pandas import DataFrame
from pandas import HDFStore
from datetime import date
from quantx.datas.cache import Cache
from quantx.factors.factor import Factor
from quantx.utils.config import Config
from quantx.utils.const import DataCol, DateFormat, DateDefault, ModCls, DataAttr
from quantx.utils.convert import ts, idict, dt
from quantx.utils.factory import cls
from quantx.utils.const import DataFill
import numpy as np


# todo lookback
class DataSetResult:
    _columns = None
    _field_idict = None
    _symbol_idict = None
    _dts = None
    _symbols = None
    _fields = None
    _cache = dict()

    def __init__(self, columns, attrs, start_offset, stop_offset):
        self._columns = columns
        self._dts = [dt(_dt) for _dt in attrs[DataCol.dt]][start_offset:stop_offset]
        self._symbols = attrs[DataCol.symbol][0]
        self._fields = attrs[DataCol.fields][0]

        self._field_idict = attrs[DataCol.fields][1]
        self._symbol_idict = attrs[DataCol.symbol][1]

    @property
    def dts(self) -> list:
        return self._dts

    @property
    def symbols(self) -> list:
        return self._symbols

    @property
    def fields(self):
        return self._fields

    def __getitem__(self, items) -> np.ndarray:
        return self._ndarray(*items)

    def _parse(self, _nd, _idict):
        if isinstance(_nd, slice):
            return slice(None)

        if isinstance(_nd, (list, tuple)):
            return [_idict[it] for it in _nd]

        return _idict[_nd]

    def _ndarray(self, dt_ixs, fields=slice(None), symbols=slice(None)):
        cname = "_".join([str(fields), str(symbols)])
        if not self._cache.__contains__(cname):
            self._cache[cname] = self._columns[:,
                                 self._parse(fields, self._field_idict),
                                 self._parse(symbols, self._symbol_idict)]

        return self._cache[cname][dt_ixs]

    def __len__(self):
        return len(self._dts)


class DataSet:
    _trading_days = None

    @property
    def cache(self) -> Cache:
        return self._trading_days

    def update(
            self,
            bundle_factor,
            dframe: DataFrame,
            anchor: tuple,
            dfill=DataFill.tail,
            dt_col=DataCol.dt,
            symbol_col=DataCol.symbol
    ):
        raise NotImplementedError

    def get(self, bundle_factor, start_date=DateDefault.start, end_date=DateDefault.end) -> DataSetResult:
        raise NotImplementedError

    def get_anchor(self, bundle_factor):
        raise NotImplementedError

    def drop(self, bundle_factor):
        raise NotImplementedError


class LocalDataSet(DataSet):
    def __init__(self, uri, cache=Config.cache_db):
        self.uri = uri
        self._trading_days = DataFrame()  # cls(cache, ModCls.cache)(uri)
        self._cache = cls(cache, ModCls.cache)(uri)

    def update(
            self,
            bundle_factor,
            dframe: DataFrame,
            anchor: tuple,
            dfill=DataFill.tail,
            dt_col=DataCol.dt,
            symbol_col=DataCol.symbol
    ):
        dframe.rename(columns={dt_col: DataCol.dt, symbol_col: DataCol.symbol}, inplace=True)

        dframe[DataCol.dt] = dt(dframe[DataCol.dt])
        dframe[DataCol.symbol] = dframe[DataCol.symbol].astype(numpy.str)
        if not isinstance(bundle_factor, Factor):
            for factor in bundle_factor.factors():
                dframe[factor.name] = dframe[factor.name].astype(factor.dtype)
        else:
            dframe[bundle_factor.name] = dframe[bundle_factor.name].astype(bundle_factor.dtype)

        with HDFStore(self.uri) as hdf:
            name = bundle_factor.name

            if dfill == DataFill.head:
                dframe = dframe.append(hdf[name])
                hdf.put(name, dframe, "t")
            else:
                hdf.put(name, dframe, "t", append=True)

            dframe = hdf[name]
            dframe[DataCol.dt] = dframe[DataCol.dt].apply(lambda x: x.value)
            dframe.set_index([DataCol.dt, DataCol.symbol], inplace=True)
            dframe.sort_index(inplace=True)
            panel = dframe.to_panel().swapaxes(0, 1)

            ca = carray(
                np.array(panel.fillna(0)).tolist(),
                rootdir=Config.get_root_file(name),
                mode="w"
            )
            ca.attrs[DataCol.dt] = [int(item) for item in panel.items]
            ca.attrs[DataCol.fields] = list(panel.major_axis), idict(list(panel.major_axis))
            ca.attrs[DataCol.symbol] = list(panel.minor_axis), idict(list(panel.minor_axis))
            ca.attrs[DataAttr.anchor] = anchor[0], (anchor[1] if anchor[1] < ts(date.today()) else ts(date.today()))

            ca.flush()
            hdf.flush(True)

    def get_anchor(self, bundle_factor):
        try:
            b = bcolz.open(Config.get_root_file(bundle_factor.name), mode="r")
            return b.attrs[DataAttr.anchor]
        except (KeyError, FileNotFoundError):
            return (None, None)

    def get(self, bundle_factor, start_date=DateDefault.start, end_date=DateDefault.end) -> DataSetResult:
        cache_name = "_".join([
            bundle_factor.name,
            dt(start_date).strftime(DateFormat.day),
            dt(end_date).strftime(DateFormat.day)
        ])
        dsr = self._cache.get(bundle_factor.name)
        if not isinstance(dsr, DataSetResult):
            ca = bcolz.open(Config.get_root_file(bundle_factor.name), mode="r")
            dts = np.array(ca.attrs[DataCol.dt])

            start = dts.searchsorted(ts(start_date))
            stop = dts.searchsorted(ts(end_date)) + 1
            dsr = DataSetResult(ca[start:stop], ca.attrs, start, stop)
            self._cache.set(cache_name, dsr)
        return dsr

    def drop(self, bundle_factor):
        try:
            with pandas.HDFStore(self.uri, mode="w") as hdf:
                hdf.remove(bundle_factor.name)
                hdf.flush(True)
        except KeyError:
            pass

            if os.path.isdir(Config.get_root_file(bundle_factor.name)):
                shutil.rmtree(Config.get_root_file(bundle_factor.name))
