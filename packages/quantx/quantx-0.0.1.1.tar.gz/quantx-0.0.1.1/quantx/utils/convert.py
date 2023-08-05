from datetime import datetime

from pandas import Timestamp, to_datetime


def symbol(x) -> str:
    return '0' * (6 - len(str(x))) + str(x)


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
    if isinstance(data, (datetime, Timestamp, type(None))):
        return data
    return to_datetime(data)
