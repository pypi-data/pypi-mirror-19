import numpy

from quantx.factors.factor import Factor
from quantx.utils.const import ModCls


class BundleMeta(type):
    def __new__(cls, name: str, bases, attrs: dict):
        if name == ModCls.bundle.split("::")[1]:
            return type.__new__(cls, name, bases, attrs)

        bundle = ""
        for n in name:
            n = "_" + n.lower() if n.isupper() else n
            bundle += n
        bundle = bundle[1:] if bundle[0] == "_" else bundle

        for inputs, factor in attrs.items():
            if isinstance(factor, (Factor,)):
                factor.inputs = [".".join([bundle, inputs])]

        return type.__new__(cls, name, bases, attrs)


class Bundle(metaclass=BundleMeta):
    pass


class MarketBundle(Bundle):
    open = Factor()
    high = Factor()
    low = Factor()
    close = Factor()
    vol = Factor()
    inc = Factor()
    active = Factor(dtype=numpy.bool)
