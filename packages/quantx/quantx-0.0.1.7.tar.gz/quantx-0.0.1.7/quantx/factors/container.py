import inspect

from dask.multiprocessing import get
from pandas import DataFrame, Series

from quantx.datas.source import Source
from quantx.factors.factor import Factor, FactorCal, CustomFactor
from quantx.utils.convert import ts


class Container:
    _source = None
    _data = None
    _dates = None

    def __init__(self, source: Source, factor, start_date, end_date):
        self._source = source
        self._factor = factor
        self._start_date = ts(start_date)
        self._end_date = ts(end_date)

    def _param_cal(self, f):
        if isinstance(f, Factor):
            return [f]

        if isinstance(f, FactorCal):
            return self._param_cal(f.factor_l) + self._param_cal(f.factor_r)

        if isinstance(f, CustomFactor):
            r_lst = [f]
            for arg in f.args + tuple(f.kwargs.values()):
                r_lst.extend(self._param_cal(arg))
            return r_lst

        return []

    def _get_factor(self, factor, start_date, end_date):

        assert isinstance(factor, (CustomFactor, Factor, FactorCal)), "不支持的因子类型[%s]" % factor.__class__
        data_dict = dict()

        for f in self._param_cal(factor):
            if isinstance(f, CustomFactor):
                data_dict[f.name] = f.f_func
            else:
                if f.bundle:
                    self._source.update(f.bundle, start_date, end_date)
                    dsr = self._source.store.get(f.bundle, start_date, end_date)
                else:
                    self._source.update(f, start_date, end_date)
                    dsr = self._source.store.get(f, start_date, end_date)

                data_dict[f.name] = DataFrame(
                    dsr[:, f.name, :],
                    index=dsr.dts,
                    columns=dsr.symbols,
                    dtype=f.dtype
                )

        if isinstance(factor, (FactorCal, CustomFactor)):
            return self._analysis(factor, data_dict).sort_index()
        if isinstance(factor, Factor):
            return data_dict[factor.name]

    def run(self):
        if isinstance(self._data, (DataFrame, Series)):
            return

        assert isinstance(
            self._factor, (
                CustomFactor,
                Factor,
                FactorCal,
                dict
            )
        ), "不支持的因子类型[%s]" % self._factor.__class__

        self._data = self._get_factor(self._factor, self._start_date, self._end_date)

    @property
    def data(self) -> DataFrame:
        return self._data

    def _analysis(self, factor_cal, params):
        raise NotImplementedError


class EvalContainer(Container):
    def _source_cal(self, f):
        if isinstance(f, Factor):
            return f.name

        if isinstance(f, FactorCal):
            return "(%s%s%s)" % (
                self._source_cal(f.factor_l),
                f.opt,
                self._source_cal(f.factor_r)
            )

        if isinstance(f, CustomFactor):
            f_akw = tuple(filter(
                lambda x: x != "",
                [
                    f.name,
                    ",".join([self._source_cal(arg) for arg in f.args]),
                    ",".join(["%s=%s" % (k, self._source_cal(v)) for k, v in f.kwargs.items()])
                ]
            ))
            return "%s(%s,%s)" % f_akw if len(f_akw) == 3 else "%s(%s)" % f_akw

        return str(f)

    def _analysis(self, factor_cal, params):
        return eval(self._source_cal(factor_cal), params)


class DaskContainer(Container):
    def _dask_cal(self, f):
        if isinstance(f, Factor):
            return f.name, {f.name: None}

        if isinstance(f, FactorCal):
            f_dict = dict()

            n_l, f_l = self._dask_cal(f.factor_l)
            n_r, f_r = self._dask_cal(f.factor_r)

            f_dict.update(f_l)
            f_dict.update(f_r)

            func_t = (f.cal, n_l, n_r)

            if f.opt in ["+", "*", "!=", "=="]:
                n = n_l + f.opt + n_r if n_l >= n_r else n_r + f.opt + n_l
            else:
                n = n_l + f.opt + n_r

            f_dict.update({n: func_t})

            return n, f_dict

        if isinstance(f, CustomFactor):
            f_dict = dict()
            params = []
            sig_params = list(inspect.signature(f.f_func).parameters.keys())
            args = list(f.args)
            kwargs = [f.kwargs[arg] for arg in sig_params[len(f.args):]]

            for arg in args + kwargs:
                n, arg_dict = self._dask_cal(arg)
                params.append(n)
                f_dict.update(arg_dict)

            n = "_".join([f.name] + params)

            f_dict[n] = tuple([f.f_func] + params)

            return n, f_dict

        n = "const_%s" % str(f)
        return n, {n: f}

    def _analysis(self, factor_cal, params):
        root, dsk = self._dask_cal(factor_cal)
        dsk.update(params)
        return get(dsk, root)
