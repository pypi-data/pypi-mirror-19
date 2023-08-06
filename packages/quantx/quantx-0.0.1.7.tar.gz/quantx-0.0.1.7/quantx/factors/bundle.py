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

        _cls = type.__new__(cls, name, bases, attrs)

        for inputs, factor in attrs.items():
            if isinstance(factor, (Factor,)):
                factor.name = ".".join([bundle, inputs])
                factor.bundle = _cls

        _cls.name = bundle
        return _cls


class Bundle(metaclass=BundleMeta):
    _columns = None
    _attrs = None
    name = None

    @classmethod
    def factors(cls):
        return [getattr(cls, attr) for attr in dir(cls) if isinstance(getattr(cls, attr), Factor)]

    @classmethod
    def get_length(cls):
        return len(list(cls.factors()))


