from pandas import Timestamp, Series, to_datetime


def symbol(x) -> str:
    return "0" * (6 - len(str(x))) + str(x)


def index(x) -> str:
    return symbol(x) + ".i"


def cls_s(cls, module=""):
    if not isinstance(cls, str):
        cls = cls.__name__
    return "".join([s.capitalize() for s in cls.split("_")] + [module])


def cls_tab(cls):
    if not isinstance(cls, str):
        cls = cls.__name__

    r = ""
    for s in cls:
        r += "_" + s.lower() if s.isupper() else s.lower()
    return r[1:]


def dt(data):
    if isinstance(data, Timestamp):
        return data

    if isinstance(data, Series):
        return to_datetime(data)

    if not data:
        return None

    return Timestamp(data)


def ts(data):
    _dt = dt(data)
    return _dt.value if _dt else None


def idict(lst):
    _dict = dict()
    for i in range(len(lst)):
        _dict[lst[i]] = i
    return _dict
