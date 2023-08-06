from datetime import datetime
from enum import Enum
from pandas import Timestamp


class Orient(Enum):
    dframe = 1
    list = 2


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
    start = Timestamp(year=1989, month=6, day=4)  # "1989-06-04"
    end = Timestamp(datetime.now())
    year = 250


class ModCls:
    dataset = "quantx.datas.dataset::DataSet"
    source = "quantx.datas.source::Source"
    bundle = "quantx.factors.bundle::Bundle"
    cache = "quantx.datas.cache::Cache"
    container = "quantx.factors.container::Container"


class Bar:
    open = "open"
    high = "high"
    low = "low"
    close = "close"
    volume = "vol"
    active = "active"
    lot = "lot"
    inc = "inc"
    quote = close


class EventType:
    INITIALIZE = "initialize"
    DAY_START = "day_start"
    HANDLE_BAR = "handle_bar"
    DAY_END = "day_end"
    SCHEDULER = "scheduler"


class OrderStat:
    OPEN = "open"
    PART = "part"
    FINISH = "finish"
    CANCEL = "cancel"
    REJECTED = "rejected"


class Func:
    initialize = "initialize"
    handle_bar = "handle_bar"
    before_trading_start = "before_trading_start"
    after_trading_end = "after_trading_end"


class EngineType:
    dask = "dask"
    eval = "eval"


class DataFill(Enum):
    head = 1
    tail = 2


class Freq(Enum):
    A = 1
    Q = 2
    M = 3
    W = 4
    D = 5
