from datetime import datetime,date
from enum import Enum
from pandas import Timestamp


class BundleCls:
    market="market"


class DataSrc:
    china_scope = "china_scope"


class DataAttr:
    anchor = "anchor"


class DataCol:
    dt = "dt"
    symbol = "symbol"
    fields = "fields"


class DateFormat:
    sec = "%Y-%m-%d %H:%M:%S"
    day = "%Y-%m-%d"


class DateDefault:
    start = Timestamp(year=1989, month=6, day=4)
    end = Timestamp(date.today())
    year = 250


class ModCls:
    dataset = "quantx.datas.dataset::DataSet"
    source = "quantx.datas.source::Source"
    bundle = "quantx.factors.buildin::Bundle"
    cache = "quantx.datas.cache::Cache"
    container = "quantx.factors.container::Container"


class OrderStat:
    OPEN = "open"
    PART = "part"
    FINISH = "finish"
    CANCEL = "cancel"
    REJECTED = "rejected"


class Func:
    initialize = "initialize"
    handle_bar = "handle_bar"
    analyse = "analyse"



class DataFill(Enum):
    head = 1
    tail = 2


class Freq(Enum):
    A = 1
    Q = 2
    M = 3
    W = 4
    D = 5
